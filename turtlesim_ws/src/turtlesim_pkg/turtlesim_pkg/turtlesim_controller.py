import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from collections import deque
from threading import Timer

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(String, 'turtle_commands', self.command_callback, 10)
        self.command_queue = deque()
        self.current_timer = None
        self.executing_command = False

    def command_callback(self, msg):
        self.command_queue.append(msg.data)
        self.get_logger().info(f'O comando recebido foi: {msg.data}')
        if not self.executing_command:
            self.execute_next_command()

    def execute_next_command(self):
        if self.command_queue:
            command = self.command_queue.popleft()
            self.get_logger().info(f'O comando {command} está sendo executado')
            vx, vy, vt, time_ms = map(float, command.split())
            self.executing_command = True

            twist = Twist()
            twist.linear.x = vx
            twist.linear.y = vy
            twist.angular.z = vt
            self.publisher_.publish(twist)

            self.current_timer = Timer(time_ms / 1000.0, self.command_finished)
            self.current_timer.start()
        else:
            self.stop_turtle()

    def command_finished(self):
        self.executing_command = False
        self.execute_next_command()

    def stop_turtle(self):
        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.angular.z = 0.0
        self.publisher_.publish(twist)
        self.get_logger().info('A tartaruguinha da sorte parou')

def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
