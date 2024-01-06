# Добавляем необходимые библиотеки:
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
import xacro


def generate_launch_description(): # Обязательный модуль файла зпуска. Функция для обработки запускаемых объектов и параметров.

    # Проверяем нужно ли нам использовать сим время ???
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_ros2_control = LaunchConfiguration('use_ros2_control')

    # Обрабатываем фаил URDF
    pkg_path = os.path.join(get_package_share_directory('my_bot')) # Указываем пакет
    xacro_file = os.path.join(pkg_path,'description','robot.urdf.xacro') # Указываем путь к Xacro файлу
    # robot_description_config = xacro.process_file(xacro_file).toxml()  # ??? Создаем некую конфигурацию на основании xacro файла
    robot_description_config = Command(['xacro ', xacro_file, ' use_ros2_control:=', use_ros2_control])

    # Создаем robot_state_publisher node
    params = {'robot_description': robot_description_config, 'use_sim_time': use_sim_time} # В параметры передаем некую конфигурацию в формате XML и результат присвоения значения use_sim_time
    node_robot_state_publisher = Node( # Создаем ноду для robot_state_publisher
        package='robot_state_publisher', # Указываем пакет как в обычном запуске через терминал
        executable='robot_state_publisher', # Указываем исполняемый фаил
        output='screen', # Выходное значение ???
        parameters=[params] # Параметры указаны над функцией
    )


    # Запуск
    return LaunchDescription([  # В возврате запускаем элементы 
        DeclareLaunchArgument( # ???
            'use_sim_time', 
            default_value='false',
            description='Use sim time if true'),
        DeclareLaunchArgument( # ???
            'use_ros2_control', 
            default_value='true',
            description='Use ros2_control if true'),

        node_robot_state_publisher  # Запускаем нашу ноду
    ])
