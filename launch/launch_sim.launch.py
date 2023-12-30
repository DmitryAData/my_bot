#Подключаем необходимые для работы библиотеки.
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node



def generate_launch_description(): # Стандартная функция для подобных файлов

    package_name='my_bot' # Устанавливаем имя пакета

    # Подключаем наш лаунч фаил с аргументом для запуска симуляции.
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Подключаем лаунч файл gazebo из пакета gazebo_ros
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )

    # Подключаем симуляцию робота
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')



    # Запускаем все
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
    ])