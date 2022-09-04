from configparser import SafeConfigParser


DELIMITER = "\r\n"

class RedisCommands(object):

    def __init__(self):
        pass

# ncode py(server) to redis(client)
    @staticmethod
    def encode(res):
        result = []
        # 数组类型 格式：* 数组元素个数 \r\n 其他所有类型 ( 结尾不需要\r\n)
        result.append("*")
        # the res is 'list' type, each array has a couple [key, value], so len*2
        result.append(str(len(res)*2))
        result.append(DELIMITER)
        for arg in res:
            for test in arg:
                # 字符串类型 格式：$ 字符串的长度 \r\n 字符串 \r\n
                result.append("$")
                result.append(str(len(test)))
                result.append(DELIMITER)
                result.append(test)
                result.append(DELIMITER)
        return "".join(result)

    @staticmethod
    def encode_new(res):
        result = []
        result.append("*")
        result.append(str(len(res)))
        result.append(DELIMITER)
        for arg in res:
            result.append("$")
            result.append(str(len(arg)))
            result.append(DELIMITER)
            result.append(arg)
            result.append(DELIMITER)
        return "".join(result)

    @staticmethod
    def encode_keys(res):
        # 数组类型 格式：* 数组元素个数 \r\n 其他所有类型 ( 结尾不需要\r\n)
        result = []
        result.append("*")
        result.append(str(len(res)))
        result.append(DELIMITER)
        # 字符串类型 格式：$ 字符串的长度 \r\n 字符串 \r\n
        for arg in res:
            result.append("$")
            result.append(str(len(arg)))
            result.append(DELIMITER)
            result.append(str(arg))
            result.append(DELIMITER)

    @staticmethod
    def set_config(key, value):
        # real action is write something into config/info
        # flag is to compare key is or not exist
        flag = 0
        with open('config/info','r') as f:
            lines = f.readlines()
        with open ('config/info','w') as m:
            for line in lines:
                l = line.strip().split()
                # if exist ,change
                if l[0]== key:
                    flag = 1
                    l[1] = value
                    new_line = " ".join(l)
                    m.write(new_line+"\r\n")
                else:
                    m.write(line)
        print("ok")
        return flag

    @staticmethod
    def parse_config(param):
        l = []
        input = open('config/info','r')
        data = input.readlines()
        pos = param.find("*")
        for i in data:
            # print all
            if param == "*":
                # len>1 -> key and value exist
                if len(i.strip().split()) > 1:
                    # string to array
                    l.append(i.strip().split())

            # find * position
            elif pos != 0 and pos != -1:
                if len(i.strip().split()) > 1 and i.startswith(param[:pos]):
                    l.append(i.strip().split())

            # if no *
            elif pos == -1:
                if len(i.strip().split()) > 1 and i.startswith(param):
                    l.append(i.strip().split())
            print(l)
            red_enc_data = RedisCommands.encode(l)

    @staticmethod
    def parse_info(time, connectionsNB, cmdsNB):
        s = []
        # change with connection and time
        parser = SafeConfigParser()
        parser.read('redis.conf')
        parser.set('info', 'uptime_in_seconds', str(time))
        parser.set('info', 'total_connections_received', str(connectionsNB))
        parser.set('info', 'total_commands_processed', str(cmdsNB))
        with open('redis.conf', 'w') as configfile:
            parser.write(configfile)
        parser.read('redis.conf')
        someinfo = parser.items('info')
        for i in someinfo:
            s.append(":".join(i))
        data = RedisCommands.encode_new(s)
        return data