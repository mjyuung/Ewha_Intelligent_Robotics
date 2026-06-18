import rclpy
from rclpy.node import Node
from ros_gz_interfaces.srv import SpawnEntity
from geometry_msgs.msg import Pose


class PeriodicSpawner(Node):

    def __init__(self):

        super().__init__('trash_spawner')

        self.client = self.create_client(
            SpawnEntity,
            '/world/trash_world/create'
        )

        self.get_logger().info(
            f"service names = {self.get_service_names_and_types()}"
        )

        self.get_logger().info(
            f"service ready = {self.client.service_is_ready()}"
        )
        
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for service...")

        with open(
            "/home/minj/ros2_ws/src/trash_bot/worlds/trash_model.sdf",
            'r'
        ) as f:self.sdf_xml = f.read()

        self.count = 0
        self.timer = self.create_timer(
            5.0,
            self.spawn_object
        )

    def spawn_object(self):

        req = SpawnEntity.Request()

        req.name = f"trash_{self.count}"
        req.xml = self.sdf_xml

        req.allow_renaming = True

        initial_pose = Pose()
        initial_pose.position.x = -4.7
        initial_pose.position.y = 2.5
        initial_pose.position.z = 1.6
        req.initial_pose = initial_pose

        future = self.client.call_async(req)
        future.add_done_callback(self.spawn_callback)

        self.count += 1

    def spawn_callback(self, future):
        try:
            res = future.result()
            self.get_logger().info(
                f"Spawn result : {res}"
            )
        except Exception as e:
            self.get_logger().error(str(e))


def main(args=None):
    rclpy.init(args=args)
    node = PeriodicSpawner()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':

    main()