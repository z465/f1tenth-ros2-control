import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32

# 1. create ros2 node

class VLMDrive(Node):
    def __init__(self):
        super().__init__('f1tenth_vlm_control')

        # 2. inside this ros2 node creating 2 publishers
        # 3. publishers publish to topic: 
        # ---> /autodrive/f1tenth_1/throttle_command
        # ---> /autodrive/f1tenth_1/steering_command

        self.publisher_throttle = self.create_publisher(Float32, '/autodrive/f1tenth_1/throttle_command', 10)   # 10 is queue size 
        self.publisher_steering = self.create_publisher(Float32, '/autodrive/f1tenth_1/steering_command', 10)

        # 4. create timer to involke callback
        time_period = 0.1
        self.timer = self.create_timer(time_period, self.timer_callback)


    def timer_callback(self):
        # 5. publish message
        # 5.1 creating message data type
        msg_throttle = Float32()
        msg_steering = Float32()

        try:

            # 5.2 giving value to msg.data
            # 5.2.1 reading from the txt file generated from VLM
            
            with open("/media/sf_Qwen-VL-Series-Finetune/data/latest_action.txt", "r") as file:
                line = file.readlines()[-1].strip()
                action_text = line
            
            if action_text == "forward":
                msg_throttle.data = 0.015
                msg_steering.data = 0.0
            
            elif action_text == "backward":
                msg_throttle.data = -0.015
                msg_steering.data = 0.0

            elif action_text == "turn left":
                msg_throttle.data = 0.015
                msg_steering.data = 0.85

            elif action_text == "turn right":
                msg_throttle.data = 0.015
                msg_steering.data = -0.85

            elif action_text == "stop":
                msg_throttle.data = 0.0
                msg_steering.data = 0.0

            else:
                self.get_logger().warn("action unknwon, checking the .txt file. actions should be within" \
                                    "(forward, backward, turn left, turn right, stop)")
                msg_throttle.data = 0.0
                msg_steering.data = 0.0
                
        
        except FileNotFoundError:
            self.get_logger().warn("actions.txt not found. Stop the car")
            msg_throttle.data = 0.0
            msg_steering.data = 0.0
    

        # 5.3 publishing data
        self.publisher_throttle.publish(msg_throttle)
        self.publisher_steering.publish(msg_steering)
            


def main(args=None):
    rclpy.init(args=args)

    node = VLMDrive()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()