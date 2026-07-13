# ไฟล์: main.py
import cv2
import mediapipe as mp
from utils import calculate_angle

# นำเข้าท่าทางต่างๆ จากไฟล์ที่เราแยกไว้
from squat_logic import SquatCounter
from pushup_logic import PushupCounter

def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    
    cap = cv2.VideoCapture(0)
    
    # -----------------------------------------------------
    # ตรงนี้คือจุดเปลี่ยนท่า! อยากเล่นท่าไหน ให้เรียก Class ท่านั้น
    # -----------------------------------------------------
    tracker = SquatCounter() 
    # tracker = PushupCounter() # ถ้าอยากเล่นวิดพื้น ก็แค่ลบคอมเมนต์บรรทัดนี้ แล้วไปคอมเมนต์บรรทัดบนแทน
    
    current_exercise = tracker.__class__.__name__ # ดึงชื่อท่ามาแสดง

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # ส่งข้อมูลไปให้ tracker คำนวณ (ไม่ว่าจะเป็น Squat หรือ Pushup มันจะจัดการเอง)
            if results.pose_landmarks:
                reps, stage, angle = tracker.process(results.pose_landmarks.landmark, mp_pose, calculate_angle)
                
                # แสดงผลบนหน้าจอ
                cv2.putText(image, f'MODE: {current_exercise}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.putText(image, f'REPS: {reps}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(image, f'STAGE: {stage}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(image, f'ANGLE: {int(angle)}', (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            cv2.imshow('FormGuard AI', image)
            if cv2.waitKey(10) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()