# Arm control algorithm to pick up and drop components stored in "detetion.json"
# The program controls 5 servo motors and 1 electromagnet
import Arm
import time
import json
import RPi.GPIO as GPIO

class arm_controller:
    magnet = 18 # pin 12
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(magnet, GPIO.OUT, initial=GPIO.HIGH)

    def grab(self):
        GPIO.output(self.magnet, GPIO.HIGH)

    def release(self):
        # GPIO.output(self.magnet, GPIO.LOW)
        
        i = 0
        while(i < 100):
            time.sleep(0.08)
            GPIO.output(self.magnet, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.magnet, GPIO.HIGH)
            i = i + 1
        GPIO.output(self.magnet, GPIO.LOW)



    def get_components_from_json(file_path):
        # Load the data from the JSON file
        with open(file_path, 'r') as f:
            detections = json.load(f)

        # Create dictionaries to store the components for each category
        resistor_components = []
        capacitor_l_components = []
        led_red_components = []
        capacitor_components = []

        # Loop through each detection and extract the components by category
        for detection in detections:
            if detection['name'] == 'resistor':
                resistor_components.append(detection)
            elif detection['name'] == 'capacitor_L':
                capacitor_l_components.append(detection)
            elif detection['name'] == 'LED_red':
                led_red_components.append(detection)
            elif detection['name'] == 'capacitor':
                capacitor_components.append(detection)

        # Return a dictionary with the components for each category
        return {
            'resistor': resistor_components,
            'capacitor_L': capacitor_l_components,
            'LED_red': led_red_components,
            'capacitor': capacitor_components
        }


    # given the corrdinate of a resistor, control robot arm and magnet 
    # to pick it up then drop in specified area :)
    def sort_resistor(x_sent, y_sent):
        base = Arm.Base(90)                 #initializing objects that make up the robot arm
        shoulder = Arm.Shoulder(115)        
        elbow = Arm.Elbow(70)
        wrist = Arm.Wrist(45)
        arm_con = arm_controller()          #initializing the controller for the electromagnet

         #This function runs off of states in order to keep track of what components are doing
         # and structure the task of picking something up. update_status increments state variable
         # up to five and then resets it back to zero for all objects of the arm

        Arm.update_state(base, shoulder, elbow, wrist) 

        arm_con.grab()  #set electromaget to high

        #state 1
        if base.state == 1:
            base.update_dist(x_sent, y_sent)                    #Calculates and sets the distance between the center of the base of arm and the object
            Arm.update_distances(base, shoulder, elbow, wrist)  #Update the distance for other componenets as well
            base.point_arm(x_sent, y_sent)                      #Move the servo in the base to point the robo arm toward the object being picked up
            Arm.update_state(base, shoulder, elbow, wrist)      #Update state for arm
            time.sleep(2)

        #state 2
        if base.state == 2:
            elbow.finAngle = Arm.cosine_law_angle(elbow.fore_arm_length, elbow.humerus_length, elbow.third_side)    #Calculate the final angle for the elbow section using cosine law

            wrist.finAngle = Arm.cosine_law_angle(wrist.fore_arm_length, wrist.third_side,                          #Do the same for the wrist angle with added offsets
                                                    wrist.humerus_length) + 90 + wrist.base_angle_offset
            shoulder.finAngle = Arm.cosine_law_angle(shoulder.humerus_length, shoulder.third_side,                  #Do the same for the shoulder angle with added offsets
                                                        shoulder.fore_arm_length) - shoulder.base_angle_offset
            shoulder.interAngle = shoulder.finAngle + 50                                                            #Set intermediate angle to hold arm above final posistion
            
            wrist.interAngle = wrist.finAngle - 50                                                                  #Set intermediate angle to position wrist perp. to ground for the
                                                                                                                    #the shoulder value.
                
            if(x_sent - 340) > 0:                                      #For imbalances of height/perspective that differ with the half of the image the coordinates sent represent
                shoulder.finAngle = shoulder.finAngle - 10             #offset them to at least "- 10" in order for the magnet to make contact with component.
            else:
                shoulder.finAngle = shoulder.finAngle - 10

            elbow.set_angle_conv(elbow.finAngle)                        #Set angle of elbow to the final angle
            wrist.set_angle_conv(wrist.interAngle)                      #Set angle for wrist and shoulder to their itermediate values
            shoulder.set_angle_conv(shoulder.interAngle)
            Arm.update_state(base, shoulder, elbow, wrist)              #Update state for the arm

            time.sleep(1.5)

        #state 3
        if base.state == 3:
            Arm.slow_move_synchro(wrist, shoulder, wrist.finAngle, shoulder.finAngle, 10)       #Slowly move the wrist and shoulder from their intermediate angles to thier 
                                                                                                #final angles by small increments of (angle diff) divided by 10
            Arm.update_state(base, shoulder, elbow, wrist)                                      #Update state for arm
            time.sleep(2)   

        #state 4
        if base.state == 4:
            elbow.set_angle_conv(90)                        #After reaching the final angle that was calculated, revert back to 90 on all parts other than the base
            wrist.set_angle_conv(90)
            shoulder.set_angle_conv(90)
            Arm.update_state(base, shoulder, elbow, wrist)  #Update state for the arm
            time.sleep(2)

        #state 5
        if base.state == 5:
            base.base_servo.angle = 45                      #For the angle that the component is to be put down at, first move it to a median angle that will cause less whiplash on parts
            time.sleep(0.5)
            base.base_servo.angle = 0                       #Set the angle to the desired sorted place of component
            time.sleep(1.5)
            
            arm_con.release()                               #release the component that is attached

            Arm.update_state(base, shoulder, elbow, wrist)  #Update the state back to zero for the arm
            time.sleep(1.5)

    #function called for sorting capacitors. Identical to the resistor verision except the final spot for placing the capacitor is different
    def sort_capacitor(x_sent, y_sent):

        base = Arm.Base(90)
        shoulder = Arm.Shoulder(115)
        elbow = Arm.Elbow(70)
        wrist = Arm.Wrist(45)
        arm_con = arm_controller()
        Arm.update_state(base, shoulder, elbow, wrist)
        arm_con.grab()


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

            if(x_sent - 340) > 0:
                shoulder.finAngle = shoulder.finAngle - 10
            else:
                shoulder.finAngle = shoulder.finAngle - 10

            elbow.set_angle_conv(elbow.finAngle)
            wrist.set_angle_conv(wrist.interAngle)
            shoulder.set_angle_conv(shoulder.interAngle)
            Arm.update_state(base, shoulder, elbow, wrist)

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
            base.base_servo.angle = 90
            time.sleep(0.5)
            base.base_servo.angle = 45
            time.sleep(3)
            
            arm_con.release()

            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(3)

#function called for sorting big capacitors. Identical to the resistor verision except the final spot for placing the big capacitor is different
    def sort_capacitor_l(x_sent, y_sent):

        base = Arm.Base(90)
        shoulder = Arm.Shoulder(115)
        elbow = Arm.Elbow(70)
        wrist = Arm.Wrist(45)
        arm_con = arm_controller()
        Arm.update_state(base, shoulder, elbow, wrist)
        arm_con.grab()


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

            if(x_sent - 340) > 0:
                shoulder.finAngle = shoulder.finAngle - 10
            else:
                shoulder.finAngle = shoulder.finAngle - 10

            elbow.set_angle_conv(elbow.finAngle)
            wrist.set_angle_conv(wrist.interAngle)
            shoulder.set_angle_conv(shoulder.interAngle)
            Arm.update_state(base, shoulder, elbow, wrist)

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
            base.base_servo.angle = 90
            time.sleep(3)
            
            arm_con.release()

            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(3)

#function called for sorting led. Identical to the resistor verision except the final spot for placing the capacitor is led
    def sort_led(x_sent, y_sent):
        base = Arm.Base(90)
        shoulder = Arm.Shoulder(115)
        elbow = Arm.Elbow(70)
        wrist = Arm.Wrist(45)
        arm_con = arm_controller()
        Arm.update_state(base, shoulder, elbow, wrist)
        arm_con.grab()


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

            if(x_sent - 340) > 0:
                shoulder.finAngle = shoulder.finAngle - 10
            else:
                shoulder.finAngle = shoulder.finAngle - 10

            elbow.set_angle_conv(elbow.finAngle)
            wrist.set_angle_conv(wrist.interAngle)
            shoulder.set_angle_conv(shoulder.interAngle)
            Arm.update_state(base, shoulder, elbow, wrist)

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
            base.base_servo.angle = 135
            time.sleep(0.5)
            base.base_servo.angle = 180
            time.sleep(3)
            
            arm_con.release()

            Arm.update_state(base, shoulder, elbow, wrist)
            time.sleep(3)
            
            
    def sort_all_resistors(self):
        
        # Get the components from the JSON file
        components = self.get_components_from_json("/home/nvidia/P2_L2B_G8/Main/detection.json")
        
        #sort resistor
        resistor_components = components['resistor']
        for resistor in resistor_components:
            if resistor['confidence'] > 0.4:
                x_input = (resistor['xmin'] + resistor['xmax'])/2
                y_input = (resistor['ymin'] + resistor['ymax'])/2 
                y_input = 480 - y_input
                self.sort_resistor(x_input, y_input)

    def sort_all_capacitors(self):
        
        # Get the components from the JSON file
        components = self.get_components_from_json("/home/nvidia/P2_L2B_G8/Main/detection.json")
        
        #sort capacitor
        capacitor_components = components['capacitor']
        for capacitor in capacitor_components:
            if capacitor['confidence'] > 0.4:
                x_input = (capacitor['xmin'] + capacitor['xmax'])/2
                y_input = (capacitor['ymin'] + capacitor['ymax'])/2
                y_input = 480 - y_input
                self.sort_capacitor(x_input, y_input)


    def sort_all_capacitors_L(self):
        
        # Get the components from the JSON file
        components = self.get_components_from_json("/home/nvidia/P2_L2B_G8/Main/detection.json")
        
        #sort capacitor_L
        capacitor_l_components = components['capacitor_L']
        for capacitor_l in capacitor_l_components:
            if capacitor_l['confidence'] > 0.4:
                x_input = (capacitor_l['xmin'] + capacitor_l['xmax'])/2
                y_input = (capacitor_l['ymin'] + capacitor_l['ymax'])/2
                y_input = 480 - y_input
                self.sort_capacitor_l(x_input, y_input)

    def sort_all_led_red(self):
        # Get the components from the JSON file
        components = self.get_components_from_json("/home/nvidia/P2_L2B_G8/Main/detection.json")
        
        #sort led_red
        led_red_components = components['LED_red']
        print(led_red_components)
        for led_red in led_red_components:
            if led_red['confidence'] > 0.4:
                x_input = (led_red['xmin'] + led_red['xmax'])/2
                y_input = (led_red['ymin'] + led_red['ymax'])/2
                y_input = 480 - y_input
                self.sort_led(x_input, y_input)
    
    
    def sort_all_components(self):
        self.sort_all_led_red(self)
        self.sort_all_resistors(self)
        self.sort_all_capacitors(self)
        # self.sort_all_capacitors_L(self)
        