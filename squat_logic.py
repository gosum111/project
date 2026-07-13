# ไฟล์: squat_logic.py
class SquatCounter:
    def __init__(self):
        self.counter = 0
        self.stage = "up" # ตั้งค่าเริ่มต้น

    def process(self, landmarks, mp_pose, calculate_angle):
        """รับจุดภาพมาคำนวณเฉพาะจุดของสควอท (สะโพก, เข่า, ข้อเท้า)"""
        try:
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            angle = calculate_angle(hip, knee, ankle)
            
            # ลอจิกการนับ
            if angle > 160:
                self.stage = "up"
            elif angle < 100 and self.stage == 'up':
                self.stage = "down"
                self.counter += 1
                
            return self.counter, self.stage, angle
        except:
            return self.counter, self.stage, 0