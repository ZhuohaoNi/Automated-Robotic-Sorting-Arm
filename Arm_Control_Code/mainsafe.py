import Arm
import time
import board
import pwmio

if __name__ == "__main__":

    base = Arm.Base(0)
    shoulder = Arm.Shoulder(115)
    elbow = Arm.Elbow(70)
    wrist = Arm.Wrist(45)
    x_sent = 160
    y_sent = 240

    Arm.update_state(base, shoulder, elbow, wrist)

    # pwm = pwmio.PWMOut(board.D13, frequency = 5000, duty_cycle = 2**15)
    # pwm.duty_cycle = 0

    if base.state == 1:
        base.update_dist(x_sent, y_sent)
        Arm.update_distances(base, shoulder, elbow, wrist)
        base.point_arm(x_sent, y_sent)
        Arm.update_state(base, shoulder, elbow, wrist)
        time.sleep(2)

    if base.state == 2:
        elbow.finAngle = Arm.cosine_law_angle(elbow.fore_arm_length, elbow.humerus_length, elbow.third_side)

        wrist.finAngle = Arm.cosine_law_angle(wrist.fore_arm_length, wrist.third_side,
                                                wrist.humerus_length) + 90 + wrist.base_angle_offset
        shoulder.finAngle = Arm.cosine_law_angle(shoulder.humerus_length, shoulder.third_side,
                                                    shoulder.fore_arm_length) - shoulder.base_angle_offset
        shoulder.interAngle = shoulder.finAngle + 50
        wrist.interAngle = wrist.finAngle - 50

        elbow.set_angle_conv(elbow.finAngle)
        wrist.set_angle_conv(wrist.interAngle)
        shoulder.set_angle_conv(shoulder.interAngle)
        Arm.update_state(base, shoulder, elbow, wrist)
        
        # pwm.duty_cycle = 2 ** 16 -1

        time.sleep(1.5)

    if base.state == 3:
        Arm.slow_move_synchro(wrist, shoulder, wrist.finAngle, shoulder.finAngle, 10)
        Arm.update_state(base, shoulder, elbow, wrist)
        time.sleep(2)

    if base.state == 4:
        elbow.set_angle_conv(90)
        wrist.set_angle_conv(90)
        shoulder.set_angle_conv(90)
        Arm.update_state(base, shoulder, elbow, wrist)
        time.sleep(2)

    if base.state == 5:
        base.base_servo.angle = 0
        time.sleep(3)
        
        # pwm.duty_cycle = 0

        Arm.update_state(base, shoulder, elbow, wrist)
        time.sleep(3)




