import os
import rclpy
from rclpy.node import Node

import cv2
from cv_bridge import CvBridge, CvBridgeError

from sensor_msgs.msg import Image

class ImageSaver(Node):
    # 1. Create subscriber node
    # 2. Subscribe to topic /autodrive/f1tenth_1/front_camera
    def __init__(self):
        super().__init__("f1tenth_camera_image_saver")
        self.subscriber_camera = self.create_subscription(
            Image, 
            "/autodrive/f1tenth_1/front_camera",
            self.sub_camera_callback,
            10)
        
        self.bridge = CvBridge()
        self.frame_index = 0
        self.save_index = 1
        self.save_dir = "/media/sf_Qwen-VL-Series-Finetune/data/images"
        ## checking whether the directory exists
        os.makedirs(self.save_dir, exist_ok=True)

        self.subscriber_camera   # prevent unused variable warning

    # the subscriber's constructor and callback don't include any timer definiction. Its callback gets called as soon as it receives a message
    
    def sub_camera_callback(self, image_msg):

        self.frame_index += 1

        ## not to save full image (testing)
        if self.save_index > 600:
            return

        if self.frame_index % 4 != 0:   # approx. 0.6s one image was saved to the destination path
            return 
        
        # 3. Convert sensor_msgs/msg/Image type into png using cv2 bridge
        try:
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, desired_encoding="bgr8")
        except CvBridgeError as e:
            self.get_logger().error(str(e))
            return

        # 4. Writing the converted cv2 image into png format
        ## checking whether successfully saved
        filename = os.path.join(self.save_dir, f"camera_{self.save_index:04d}.jpg")
        success = cv2.imwrite(filename, cv_image)

        if success:
            self.get_logger().info(f"Saved {filename}")
            self.save_index += 1
        else:
            self.get_logger().error("Failed to save image")
        
        
        



def main(args=None):
    rclpy.init(args=args)

    image_saver = ImageSaver()

    rclpy.spin(image_saver)

    image_saver.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()