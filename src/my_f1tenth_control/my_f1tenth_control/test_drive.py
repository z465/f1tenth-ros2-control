import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32

# 1. create ros2 node

class TestDrive(Node):
    def __init__(self):
        super().__init__('f1tenth_control')

        # 2. inside this ros2 node creating 2 publishers
        # 3. publishers publish to topic: 
        # ---> /autodrive/f1tenth_1/throttle_command
        # ---> /autodrive/f1tenth_1/steering_command

        self.publisher_throttle = self.create_publisher(Float32, '/autodrive/f1tenth_1/throttle_command', 10)   # 10 is queue size 
        self.publisher_steering = self.create_publisher(Float32, '/autodrive/f1tenth_1/steering_command', 10)

        # 4. create timer to involke callback
        time_period = 0.1
        self.timer = self.create_timer(time_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        # 5. publish message
        # 5.1 creating message data type
        # 5.2 giving value to msg.data
        # 5.3 publishing data
        msg_throttle = Float32()
        msg_steering = Float32()
        
        if self.i < 50:
            msg_throttle.data = -0.1
            msg_steering.data = 0.0
        
        elif self.i >= 50 and self.i < 60:
            msg_throttle.data = 0.1
            msg_steering.data = -0.2

        elif self.i >= 60:
            msg_throttle.data = 0.0
            msg_steering.data = 0.0

        self.publisher_throttle.publish(msg_throttle)
        self.publisher_steering.publish(msg_steering)

        # logger
        #self.get_logger().info(f'Publishing throttle: {msg_throttle.data}')
        #self.get_logger().info(f'Publishing steering: {msg_steering.data}')

        self.i += 1
        


def main(args=None):
    rclpy.init(args=args)

    node = TestDrive()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()