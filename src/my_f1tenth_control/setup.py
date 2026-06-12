from setuptools import setup

package_name = 'my_f1tenth_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bubblegum',
    maintainer_email='bubblegum@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'test_run = my_f1tenth_control.test_drive:main',
            'image_saver = my_f1tenth_control.image_saver:main',
            'f1tenth_vlm_control = my_f1tenth_control.f1tenth_vlm_control:main',
            'f1tenth_init = my_f1tenth_control.f1tenth_init:main',
        ],
    },
)
