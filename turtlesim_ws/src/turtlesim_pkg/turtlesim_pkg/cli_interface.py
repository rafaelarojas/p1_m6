import argparse
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class CommandPublisher(Node):
    def __init__(self):
        super().__init__('command_publisher')
        self.publisher_ = self.create_publisher(String, 'turtle_commands', 10)

    def publish_command(self, command):
        msg = String()
        msg.data = command
        self.publisher_.publish(msg)
        self.get_logger().info(f'Comando publicado: {command}')

def main(args=None):
    rclpy.init(args=args)
    node = CommandPublisher()

    parser = argparse.ArgumentParser(description='Mande os movimntos para a tartaruguinha da sorte fazer')
    parser.add_argument('--vx', type=float, default=0.0, help='Velocidade da tartaruguinha na direção x')
    parser.add_argument('--vy', type=float, default=0.0, help='Velocidade da tartaruguinha na direção y')
    parser.add_argument('--vt', type=float, default=0.0, help='Velocidade angular')
    parser.add_argument('-t', '--time', type=int, required=True, help='Execução em milisegundos')

    args = parser.parse_args()

    command = f"{args.vx} {args.vy} {args.vt} {args.time}"
    node.publish_command(command)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
