import cv2
import mediapipe as mp
import serial
import time

ser = serial.Serial('COM7', 9600)  # Update 'COM3' with your Arduino's serial port

def map_range(x, in_min, in_max, out_min, out_max):
    x = max(in_min, min(in_max, x))  # Limit x to be within in_min and in_max
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def main():
    mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = mp_hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                thumb_landmark = hand_landmarks.landmark[4]
                index_landmark = hand_landmarks.landmark[8]
                middle_landmark = hand_landmarks.landmark[12]
                ring_landmark = hand_landmarks.landmark[16]
                pinky_landmark = hand_landmarks.landmark[20]

                thumb_tip_y = int(thumb_landmark.y * frame.shape[0])
                index_tip_y = int(index_landmark.y * frame.shape[0])
                middle_tip_y = int(middle_landmark.y * frame.shape[0])
                ring_tip_y = int(ring_landmark.y * frame.shape[0])
                pinky_tip_y = int(pinky_landmark.y * frame.shape[0])

                # Increase the sensitivity by using a smaller range of openness values
                thumb_openness = thumb_tip_y - index_tip_y
                index_openness = index_tip_y - middle_tip_y
                middle_openness = middle_tip_y - ring_tip_y
                ring_openness = ring_tip_y - pinky_tip_y
                pinky_openness = pinky_tip_y - ring_tip_y

                # Adjust the sensitivity by changing the range for each finger
                thumb_angle = map_range(thumb_openness, 30, 150, 0, 180)
                index_angle = map_range(index_openness, 10,30 , 0, 180)
                middle_angle = map_range(middle_openness, 0, 120, 0, 180)
                ring_angle = map_range(ring_openness, 0, 120, 0, 180)
                pinky_angle = map_range(pinky_openness, 30, 150, 0, 180)

                # Send the finger angles to Arduino over serial
                if thumb_angle!=0 and index_angle==0 and pinky_angle==0 :
                    ser.write("1".encode())

                elif thumb_angle!=0 and index_angle!=0 and pinky_angle==0 :
                    ser.write("5".encode())
                elif thumb_angle!=0 and index_angle!=0 and pinky_angle!=0:
                    ser.write("3".encode())


                # Draw circles on the finger tips (optional, for visualization)
                thumb_tip_x = int(thumb_landmark.x * frame.shape[1])
                index_tip_x = int(index_landmark.x * frame.shape[1])
                middle_tip_x = int(middle_landmark.x * frame.shape[1])
                ring_tip_x = int(ring_landmark.x * frame.shape[1])
                pinky_tip_x = int(pinky_landmark.x * frame.shape[1])

                cv2.circle(frame, (thumb_tip_x, thumb_tip_y), 5, (0, 255, 0), -1)
                cv2.circle(frame, (index_tip_x, index_tip_y), 5, (0, 255, 0), -1)
                cv2.circle(frame, (middle_tip_x, middle_tip_y), 5, (0, 255, 0), -1)
                cv2.circle(frame, (ring_tip_x, ring_tip_y), 5, (0, 255, 0), -1)
                cv2.circle(frame, (pinky_tip_x, pinky_tip_y), 5, (0, 255, 0), -1)

                # Print the finger angles to the terminal
                print(f"Thumb angle: {thumb_angle}, Index angle: {index_angle}, Middle angle: {middle_angle}, Ring angle: {ring_angle}, Pinky angle: {pinky_angle}")

        cv2.imshow('Hand Tracking', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)  # Introduce a delay to prevent overwhelming the serial communication

    cap.release()
    cv2.destroyAllWindows()
    ser.close()



if __name__ == "__main__":
    main()