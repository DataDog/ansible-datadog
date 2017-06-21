import socket
import subprocess

from checks import AgentCheck


class DockerSwarm(AgentCheck):

    def check(self, instance):
        metric = "docker_swarm.running"
        host_name = socket.gethostbyname(socket.gethostname())
        tag = 'host:%s' % host_name

        pipes = subprocess.Popen("sudo docker node ls",stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        std_out, std_err = pipes.communicate()
        returncode = pipes.returncode

        if returncode:
            self.gauge(metric, returncode, tags=[tag])
        else:
            self.gauge(metric, -1, tags=[tag])