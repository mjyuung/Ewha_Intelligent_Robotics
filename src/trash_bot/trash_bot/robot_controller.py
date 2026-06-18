import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from std_msgs.msg import String

class BodyController(Node):
    def __init__(self):
        super().__init__('body_controller')
        self.subscription = self.create_subscription(
            String,
            '/body_controll',
            self.body_controll_callback,
            10)
        self.subscription
        
        self.get_logger().info('LidarSubscriber started — listening on /scan')

    def body_controll_callback(self, msg):
        if msg.data=="go": self.send_joint_goal

    def send_joint_goal(self):
        # Initialize node
        rclpy.init()
        node = rclpy.create_node('joint_commander')
        action_client = ActionClient(node, FollowJointTrajectory, '/arm_controller/follow_joint_trajectory')

        # Wait for action server
        action_client.wait_for_server()

        # Create goal message
        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory.joint_names = ['joint_1', 'joint_2']
        
        point = JointTrajectoryPoint()
        point.positions = [1.5, -0.5]
        point.time_from_start.sec = 2 # Reach position in 2 seconds
        
        goal_msg.trajectory.points = [point]

        # Send goal and wait for result
        future = action_client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(node, future)
        
        node.get_logger().info('Goal sent successfully!')
        node.destroy_node()
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = BodyController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

