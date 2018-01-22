from tool import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import StartInstanceRequest, StopInstanceRequest

client = AcsClient(settings.ACS_KEY, settings.ACS_SECRET, settings.ACS_ENDPOINT)


def start():
    request = StartInstanceRequest.StartInstanceRequest()
    request.set_InstanceId(settings.ACS_INSTANT_ID)
    resp = client.do_action_with_exception(request)

    print(resp)


def stop():
    request = StopInstanceRequest.StopInstanceRequest()
    request.set_InstanceId('i-uf65cpnw0xewj6niwaju')
    resp = client.do_action_with_exception(request)

    print(resp)


if __name__ == '__main__':
    import sys

    if sys.argv[1] == 'stop':
        stop()
    elif sys.argv[1] == 'start':
        start()
