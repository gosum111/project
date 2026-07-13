# ไฟล์: pushup_logic.py
class PushupCounter:
    def __init__(self):
        self.counter = 0
        self.stage = "up"

    def process(self, landmarks, mp_pose, calculate_angle):
        """รับจุดภาพมาคำนวณเฉพาะจุดของวิดพื้น (ไหล่, ศอก, ข้อมือ)"""
        try:
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            angle = calculate_angle(shoulder, elbow, wrist)
            
            # ลอจิกการนับ (ตัวเลขสมมติ ต้องไปปรับแก้ตามจริง)
            if angle > 160:
                self.stage = "up"
            elif angle < 90 and self.stage == 'up':
                self.stage = "down"
                self.counter += 1
                
            return self.counter, self.stage, angle
        except:
            return self.counter, self.stage, 0