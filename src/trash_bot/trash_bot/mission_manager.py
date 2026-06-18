import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseStamped
from trajectory_msgs.msg import JointTrajectoryPoint
from nav2_msgs.action import NavigateToPose
from control_msgs.action import FollowJointTrajectory

states_dict = {"idle": 0, "move": 0, "up": 1, "down": 0, "return": 1}

WAYPOINTS = [
    ( 13.0,  -3.5,  0.0 ),
    ( 0.0,  0.0,   0.0 ),
]

JOINTPOINTS = [ [0.0], [3.0] ]

def make_pose(x, y, yaw_deg, clock):
    yaw = math.radians(yaw_deg)
    p = PoseStamped()
    p.header.frame_id = 'map'
    p.header.stamp = clock.now().to_msg()
    p.pose.position.x = x
    p.pose.position.y = y
    p.pose.orientation.z = math.sin(yaw / 2.0)
    p.pose.orientation.w = math.cos(yaw / 2.0)
    return p

class MissionManager(Node):
    def __init__(self):
        super().__init__('mission_manager')

        self.lidar_sub = self.create_subscription(
            LaserScan,
            '/scan1',
            self.scan_callback,
            10,
        )

        self._client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self._client.wait_for_server()

        self.joint_client = ActionClient(
            self,
            FollowJointTrajectory,
            '/joint_trajectory_controller/follow_joint_trajectory'
        )

        self.joint_client.wait_for_server()
        self._current_state = "idle"

    def scan_callback(self, msg: LaserScan):
        if self._current_state != "idle": return

        front_range = min(msg.ranges)

        # Replace nan/inf with a readable string
        if front_range != front_range or front_range == float('inf'):
            self.get_logger().warn('out of bound')
        else:
            if front_range < 0.5:
                self._current_state = "move"
                self.send_nav2()


    def send_nav2(self):
        if self._current_state != "move" and self._current_state != "return": return

        x, y, yaw = WAYPOINTS[states_dict.get(self._current_state)]
        self.get_logger().info(
            f'Navigating to ({x:.2f}, {y:.2f}, {yaw:.0f}°)')
        goal = NavigateToPose.Goal()
        goal.pose = make_pose(x, y, yaw, self.get_clock())
        self._client.send_goal_async(goal).add_done_callback(
            lambda f: f.result().get_result_async().add_done_callback(self.on_result)
            if f.result().accepted else self.get_logger().warn('Goal rejected'))

    def on_result(self, future):
        if future.result().status == GoalStatus.STATUS_SUCCEEDED:
            if self._current_state == "move":
                self._current_state = "up"
                self.send_joint_goal()
            else:
                self._current_state = "idle"
        else:
            self.get_logger().warn('Navigation failed at waypoint')

    def send_joint_goal(self):
        if self._current_state != "up" and self._current_state != "down": return

        goal = FollowJointTrajectory.Goal()

        goal.trajectory.joint_names = ['cylinder_joint']
        point = JointTrajectoryPoint()
        point.positions = JOINTPOINTS[states_dict.get(self._current_state)]
        point.velocities = [0.0]
        point.time_from_start.sec = 10

        goal.trajectory.points = [point]

        self.get_logger().info(f'Send joint goal {point.positions}')

        future = self.joint_client.send_goal_async(goal)

        future.add_done_callback(self.joint_goal_response)

    def joint_goal_response(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().warn('Joint goal rejected')
            return

        self.get_logger().info('Joint goal accepted')

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.joint_result)

    def joint_result(self, future):
        self.get_logger().info(
            'Joint motion finished'
        )

        if self._current_state == 'up':
            self._current_state = 'down'
            self.send_joint_goal()

        elif self._current_state == 'down':
            self._current_state = 'return'
            self.send_nav2()


def main(args=None):
    rclpy.init(args=args)
    node = MissionManager()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
