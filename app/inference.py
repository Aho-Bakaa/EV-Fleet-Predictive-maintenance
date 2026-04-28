import joblib
import numpy as np
import pandas as pd
from typing import Dict, List
from datetime import datetime

from app.config import (
    MODELS_DIR,
    SOH_MODEL_PATH,
    RUL_MODEL_PATH,
    THERMAL_MODEL_PATH,
    SOH_SCALER_PATH,
    RUL_SCALER_PATH,
    THERMAL_SCALER_PATH,
    FEATURE_COLUMNS,
    SOH_CRITICAL_THRESHOLD,
    SOH_WARNING_THRESHOLD,
    RUL_URGENT_THRESHOLD,
    THERMAL_DANGER_THRESHOLD,
    MODEL_VERSION
)
class EVMaintenancePredictor:
   
    def __init__(self):
        print("Loading models...")
        self.soh_model = None
        self.rul_model = None
        self.thermal_model = None
        
        self.soh_scaler = None
        self.rul_scaler = None
        self.thermal_scaler = None
        
        self.feature_columns = FEATURE_COLUMNS
        
        self._load_models()
        print("Models loaded successfully!")
    def _load_models(self):

        try:
            if SOH_MODEL_PATH.exists() and SOH_SCALER_PATH.exists():
                self.soh_model = joblib.load(SOH_MODEL_PATH)
                self.soh_scaler = joblib.load(SOH_SCALER_PATH)
            else:
                raise FileNotFoundError(f"SOH model files not found in {MODELS_DIR}")
            
            if RUL_MODEL_PATH.exists() and RUL_SCALER_PATH.exists():
                self.rul_model = joblib.load(RUL_MODEL_PATH)
                self.rul_scaler = joblib.load(RUL_SCALER_PATH)
            else:
                raise FileNotFoundError(f"RUL model files not found in {MODELS_DIR}")
            
            if THERMAL_MODEL_PATH.exists() and THERMAL_SCALER_PATH.exists():
                self.thermal_model = joblib.load(THERMAL_MODEL_PATH)
                self.thermal_scaler = joblib.load(THERMAL_SCALER_PATH)
            else:
                raise FileNotFoundError(f"Thermal model files not found in {MODELS_DIR}")
                
        except Exception as e:
            print(f" Error loading models: {e}")
            raise

    def _preprocess_input(self, vehicle_data: Dict, feature_columns: List[str], scaler) -> np.ndarray:
       
        df = pd.DataFrame([vehicle_data])
        try:
            X = df[self.feature_columns]
        except KeyError as e:
            missing_features = set(self.feature_columns) - set(df.columns)
            raise ValueError(f"Missing required features: {missing_features}")
        
        X = X.fillna(0)
        X_scaled = scaler.transform(X)
        
        return X_scaled
    def predict(self, vehicle_data: Dict) -> Dict:
       
        try:
            X_soh = self._preprocess_input(vehicle_data, self.feature_columns, self.soh_scaler)
            X_rul = self._preprocess_input(vehicle_data, self.feature_columns, self.rul_scaler)
            X_thermal = self._preprocess_input(vehicle_data, self.feature_columns, self.thermal_scaler)
            
            soh_pred = float(self.soh_model.predict(X_soh)[0])
            soh_pred = max(0.0, min(1.0, soh_pred))

            rul_pred = float(self.rul_model.predict(X_rul)[0]) 
            thermal_pred = float(self.thermal_model.predict(X_thermal)[0])
            
            rul_cycles = int(rul_pred)
            rul_days = int(rul_cycles / 2) 
            
            alert = self._generate_alert(soh_pred, rul_cycles, thermal_pred)
            
            return {
                'vehicle_id': vehicle_data.get('Vehicle_ID', 'unknown'),
                'timestamp': datetime.now().isoformat(),
                'model_version': MODEL_VERSION,
                'predictions': {
                    'soh': round(soh_pred, 4),
                    'soh_percentage': f"{soh_pred:.1%}",
                    'rul_cycles': rul_cycles,
                    'rul_days': rul_days,
                    'thermal_risk_score': round(thermal_pred, 4),
                    'thermal_risk_percentage': f"{thermal_pred:.1%}"
                },
                'alert': alert,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error_message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    def _generate_alert(self, soh: float, rul: int, thermal_risk: float) -> Dict:

        if thermal_risk > THERMAL_DANGER_THRESHOLD:
            return {
                'level': 'CRITICAL',
                'priority': 1,
                'message': f' High thermal runaway risk detected ({thermal_risk:.1%})',
                'actions': [
                    'Stop vehicle immediately',
                    'Do not charge',
                    'Inspect battery pack',
                    'Contact emergency services if overheating'
                ]
            }
        
        if soh < SOH_CRITICAL_THRESHOLD:
            return {
                'level': 'CRITICAL',
                'priority': 1,
                'message': f' Battery end-of-life (SOH: {soh:.1%})',
                'actions': [
                    'Schedule battery replacement immediately',
                    'Do not fast charge',
                    'Limit usage to essential trips only'
                ]
            }
        
        if rul < RUL_URGENT_THRESHOLD:
            return {
                'level': 'URGENT',
                'priority': 2,
                'message': f' Battery replacement needed soon ({rul} cycles remaining)',
                'actions': [
                    'Schedule replacement within 2 weeks',
                    'Monitor SOH daily',
                    'Avoid extreme temperatures'
                ]
            }
        if soh < SOH_WARNING_THRESHOLD:
            return {
                'level': 'WARNING',
                'priority': 3,
                'message': f' Battery degradation detected (SOH: {soh:.1%})',
                'actions': [
                    'Schedule inspection within 1 month',
                    'Monitor performance',
                    'Plan for replacement'
                ]
            }
        return {
            'level': 'OK',
            'priority': 4,
            'message': ' Battery healthy',
            'actions': [],
            'color': 'green'
        }
