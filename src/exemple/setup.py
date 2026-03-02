from setuptools import find_packages, setup

package_name = 'exemple'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gan',
    maintainer_email='3823969377@qq.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "new_node=exemple.test:main",
            "pub_sum_node=exemple.pub_num:main",
            "sub_sum_node=exemple.sub_num:main"
        ],
    },
)
