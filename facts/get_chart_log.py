#!/usr/local/bin/python
import glob
import pandas as pd
import time
import numpy as np
import datetime
import os
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import ScalarFormatter 
import matplotlib
import platform
import itertools

#name_list=['slt28-palm']
#name_list_tcs=['slt11-orchid','pdt-honey','nonibert','slt104-orange','slt112-pe','poetry','botree','f17-44','slt112-onager','greatwall-a','qinguo-2','shanhai','pdt-pitaya','pdt-pepper','pdt-pumpkin','pdt-berry','pdt-melon','slt13-carrot']
#name_list_tcs=['slt11-orchid','pdt-honey','nonibert','slt104-orange','slt112-pe','poetry','botree','f17-44','slt112-onager','greatwall-a','qinguo-2','shanhai','pdt-melon','peace','pdt-pitaya','pdt-mango','pdt-peach']
name_list_minipdt=['gw-minipdt-quincy1','pdt-xian','pdt-tongchuan','slt28-palm','pdt-xian-2','pdt-tongchuan-2','nonibert','qinguo-2','shanhai','qinguo']
#name_list_regression=['calla', 'g07-31', 'qiguo', 'pdt-yulin-2', 'slt13-celery', 'qinguo', 'pdt-reed', 'pdt-summer', 'ibmdow-reg2', 'slt60-loquat', 'slt17-balsam', 'prose', 'pdt-gw11', 'pdt-weinan', 'slt105-shanquan', 'g07-28', 'slt17-begonia', 'yanmen', 'slt15-ginseng', 'slt104-grape', 'slt106-tmac', 'slt105-j7', 'pdt-waxberry', 'slt12-anemone', 'slt103-cicada', 'pdt-venus', 'slt113-raptors', 'pdt-orange', 'pdt-mercury', 'slt60-j7', 'greatwall-b', 'g07-27', 'pdt-weinan-2', 'slt102-mamba', 'pdt-mars', 'pdt-yanan-2', 'slt106-kb', 'slt112-warriors', 'slt15-medlar', 'zhaoguo-2', 'slt102-cobra', 'moonlight', 'pdt-longan', 'g07-29', 'forge-lsys1', 'slt102-python', 'weiguo-2', 'slt11-rose', 'slt103-cricket', 'pdt-lotus', 'slt111-opium', 'pdt-earth', 'pdt-gw12', 'lonibert', 'attacking', 'slt28-pine', 'slt123-north', 'slt113-cavaliers', 'slt123-pyke', 'paper', 'chuguo-2', 'smily-vsrx', 'gw-minipdt-quincy2', 'pdt-pumpkin', 'slt17-j7', 'slt111-morphia', 'slt60-lemon', 'qiguo-2', 'choko', 'pdt-yanan', 'slt103-j7', 'slt106-ai', 'pdt-xianyang', 'pdt-pepper', 'guo', 'pdt-berry', 'pdt-lemon', 'forge-lsys2', 'sunshine', 'slt123-wyk', 'pdt-coconut', 'slt13-carrot', 'slt12-jasmine', 'pdt-yulin', 'pdt-winter', 'pdt-casaba', 'slt102-adder', 'wan', 'defending', 'pdt-xianyang-2', 'slt112-spurs', 'ibmdow-reg1', 'hanguo-2', 'slt123-wall', 'slt105-nongfu', 'honor-vsrx']
name_list_tcs=['slt11-orchid', 'slt11-rose', 'slt112-pe', 'botree', 'f17-44', 'slt112-onager', 'greatwall-a', 'greatwall-b', 'qinguo-2', 'qiguo-2', 'slt104-orange', 'slt104-grape', 'shanhai', 'yanmen', 'poetry', 'prose', 'peace', 'paper', 'pdt-pepper', 'pdt-pumpkin', 'pdt-honey', 'pdt-waxberry', 'nonibert', 'lonibert', 'slt13-carrot', 'slt13-celery', 'pdt-melon', 'pdt-orange', 'pdt-coconut', 'pdt-longan', 'pdt-pitaya', 'pdt-mango', 'pdt-peach', 'pdt-berry', 'pdt-lemon', 'pdt-casaba', 'pdt-xian', 'pdt-xianyang', 'pdt-weinan', 'pdt-tongchuan', 'pdt-yanan', 'pdt-yulin']
tcs_owner_dict={'crachakonda': ['slt11-orchid', 'slt11-rose', 'slt112-pe', 'botree', 'f17-44', 'slt112-onager', 'greatwall-a', 'greatwall-b', 'qinguo-2', 'qiguo-2'],
                'kchintada': ['pdt-honey', 'pdt-waxberry', 'nonibert', 'lonibert', 'slt13-carrot', 'slt13-celery', 'pdt-melon', 'pdt-orange', 'pdt-coconut', 'pdt-longan'],
				'rvantari': ['pdt-pitaya', 'pdt-mango', 'pdt-peach', 'pdt-berry', 'pdt-lemon', 'pdt-casaba', 'pdt-xian', 'pdt-xianyang', 'pdt-weinan', 'pdt-tongchuan', 'pdt-yanan', 'pdt-yulin'],
				'hparvathanen': ['poetry', 'prose', 'peace', 'paper', 'pdt-pepper', 'pdt-pumpkin'],
				'udronamraju': ['slt104-orange', 'slt104-grape', 'shanhai', 'yanmen']}
name_list_regression=['kvm-dhcp','zinnia','calla', 'slt103-cicada', 'pdt-venus', 'pdt-mercury', 'pdt-mars', 'slt103-cricket', 'pdt-earth', 'choko', 'slt103-j7', 'guo', 'wan', 'pdt-jupiter', 'pdt-saturn', 'qiguo', 'qinguo', 'forge-lsys1', 'forge-lsys2', 'forge-pdt-10', 'forge-pdt-11', 'pdt-gw5', 'pdt-gw6', 'slt12-anemone', 'slt12-jasmine', 'fig', 'yam', 'slt60-cactus', 'slt60-clove', 'ibmdow-reg2', 'pdt-gw11', 'moonlight', 'pdt-gw12', 'sunshine', 'ibmdow-reg1', 'pdt-reed', 'slt105-shanquan', 'slt105-j7', 'pdt-lotus', 'slt28-pine', 'gw-minipdt-quincy2', 'slt105-nongfu', 'slt28-palm', 'gw-minipdt-quincy1', 'slt7-tulip', 'slt7-lilac', 'pdt-summer', 'slt113-raptors', 'slt112-warriors', 'slt111-opium', 'slt113-cavaliers', 'slt111-morphia', 'pdt-winter', 'slt112-spurs', 'slt60-loquat', 'slt17-balsam', 'slt17-begonia', 'slt15-ginseng', 'slt60-j7', 'slt15-medlar', 'slt17-j7', 'slt60-lemon', 'pdt-thor', 'pdt-hulk', 'f13-33', 'f13-34', 'f14-23', 'f16-40', 'f16-42', 'pdt-forge-natt', 'f15-34', 'f15-36', 'pdt-yulin-2', 'pdt-weinan-2', 'pdt-yanan-2', 'attacking', 'defending', 'pdt-xianyang-2', 'pdt-sparrow', 'pdt-swallow', 'pdt-magpie', 'pdt-phoenix', 'pdt-seagull', 'pdt-tongchuan-2', 'pdt-xian-2', 'g07-31', 'g07-28', 'slt106-tmac', 'g07-27', 'slt102-mamba', 'slt106-kb', 'slt102-cobra', 'g07-29', 'slt102-python', 'slt123-north', 'slt123-pyke', 'smily-vsrx', 'slt106-ai', 'slt123-wyk', 'slt102-adder', 'slt123-wall', 'honor-vsrx', 'smily-peer']
#cnrd_owner_dict={'deanchen': ['calla', 'slt103-cicada', 'pdt-venus', 'pdt-mercury', 'pdt-mars', 'slt103-cricket', 'pdt-earth', 'choko', 'slt103-j7', 'guo', 'wan'], 'ztao': ['qiguo', 'qinguo', 'forge-lsys1', 'forge-lsys2'], 'yangchen': ['slt12-anemone', 'slt12-jasmine'], 'arieszhan': ['ibmdow-reg2', 'pdt-gw11', 'moonlight', 'pdt-gw12', 'sunshine', 'ibmdow-reg1'], 'haliu': ['pdt-reed', 'slt105-shanquan', 'slt105-j7', 'pdt-lotus', 'slt28-pine', 'gw-minipdt-quincy2', 'slt105-nongfu'], 'emilydu': ['pdt-summer', 'slt113-raptors', 'slt112-warriors', 'slt111-opium', 'slt113-cavaliers', 'slt111-morphia', 'pdt-winter', 'slt112-spurs'], 'darrenli': ['slt60-loquat', 'slt17-balsam', 'slt17-begonia', 'slt15-ginseng', 'slt60-j7', 'slt15-medlar', 'slt17-j7', 'slt60-lemon'], 'arielwei': ['pdt-yulin-2', 'pdt-weinan-2', 'pdt-yanan-2', 'attacking', 'defending', 'pdt-xianyang-2'], 'ryanliu': ['g07-31', 'g07-28', 'slt106-tmac', 'g07-27', 'slt102-mamba', 'slt106-kb', 'slt102-cobra', 'g07-29', 'slt102-python', 'slt123-north', 'slt123-pyke', 'smily-vsrx', 'slt106-ai', 'slt123-wyk', 'slt102-adder', 'slt123-wall', 'honor-vsrx']}
cnrd_owner_dict={'deanchen': ['calla', 'slt103-cicada', 'pdt-venus', 'pdt-mercury', 'pdt-mars', 'slt103-cricket', 'pdt-earth', 'choko', 'slt103-j7', 'guo', 'wan', 'pdt-jupiter', 'pdt-saturn'], 
                 'ztao': ['qiguo', 'qinguo', 'forge-lsys1', 'forge-lsys2', 'forge-pdt-10', 'forge-pdt-11', 'pdt-gw5', 'pdt-gw6'], 
				 'yangchen': ['slt12-anemone', 'slt12-jasmine','fig', 'yam', 'slt60-cactus', 'slt60-clove'], 
				 'arieszhan': ['ibmdow-reg2', 'pdt-gw11', 'moonlight', 'pdt-gw12', 'sunshine', 'ibmdow-reg1'],
				 'haliu': ['pdt-reed', 'slt105-shanquan', 'slt105-j7', 'pdt-lotus', 'slt28-pine', 'gw-minipdt-quincy2', 'slt105-nongfu', 'slt28-palm', 'gw-minipdt-quincy1', 'slt7-tulip', 'slt7-lilac'], 
				 'emilydu': ['pdt-summer', 'slt113-raptors', 'slt112-warriors', 'slt111-opium', 'slt113-cavaliers', 'slt111-morphia', 'pdt-winter', 'slt112-spurs'], 
				 'darrenli': ['slt60-loquat', 'slt17-balsam', 'slt17-begonia', 'slt15-ginseng', 'slt60-j7', 'slt15-medlar', 'slt17-j7', 'slt60-lemon', 'pdt-thor', 'pdt-hulk', 'f13-33', 'f13-34', 'f14-23', 'f16-40', 'f16-42', 'pdt-vsrx04', 'pdt-forge-natt', 'f15-34', 'f15-36'], 
				 'arielwei': ['pdt-yulin-2', 'pdt-weinan-2', 'pdt-yanan-2', 'attacking', 'defending', 'pdt-xianyang-2', 'pdt-sparrow', 'pdt-swallow', 'pdt-magpie', 'pdt-phoenix', 'pdt-seagull', 'pdt-tongchuan-2', 'pdt-xian-2'], 
				 'ryanliu': ['kvm-dhcp','zinnia','g07-31', 'g07-28', 'slt106-tmac', 'g07-27', 'slt102-mamba', 'slt106-kb', 'slt102-cobra', 'g07-29', 'slt102-python', 'slt123-north', 'slt123-pyke', 'smily-vsrx', 'slt106-ai', 'slt123-wyk', 'slt102-adder', 'slt123-wall', 'honor-vsrx', 'smily-peer']}
name_list=['qinguo-2','nonibert','gw-minipdt-quincy1','pdt-xian','pdt-tongchuan','slt28-palm','slt17-balsam','slt11-orchid','slt15-medlar','pdt-xian-2','pdt-tongchuan-2']

#name_list=['pdt-thor', 'pdt-hulk', 'f13-33', 'f13-34', 'f14-23', 'f16-40', 'f16-42', 'pdt-vsrx05', 'pdt-vsrx06', 'pdt-vsrx07', 'pdt-vsrx08', 'pdt-vsrx09', 'f15-34', 'f15-36', 'pdt-forge-natt', 'pdt-vsrx01', 'pdt-vsrx02', 'pdt-vsrx03', 'pdt-vsrx04', 'smily-vsrx', 'honor-vsrx', 'smily-peer', 'slt60-lemon', 'slt60-loquat', 'slt60-j7', 'slt60-cactus', 'slt60-clove', 'slt123-wyk', 'slt123-pyke', 'slt123-north', 'slt123-wall', 'zinnia', 'g07-27', 'g07-28', 'g07-29', 'g07-31', 'kvm-dhcp', 'slt106-kb', 'slt106-ai', 'slt106-tmac', 'poetry', 'prose', 'peace', 'paper', 'pdt-honey', 'pdt-waxberry', 'pdt-gw11', 'pdt-gw12', 'attacking', 'defending', 'slt104-orange', 'slt104-grape', 'pdt-pitaya', 'pdt-mango', 'pdt-peach', 'forge-pdt-10', 'forge-pdt-11', 'pdt-gw5', 'pdt-gw6', 'slt112-pe', 'botree', 'f17-44', 'slt112-onager', 'pdt-melon', 'pdt-orange', 'pdt-coconut', 'pdt-longan', 'pdt-berry', 'pdt-lemon', 'pdt-casaba', 'slt102-python', 'slt102-cobra', 'slt102-adder', 'slt102-mamba', 'slt13-carrot', 'slt13-celery', 'slt15-medlar', 'slt15-ginseng', 'slt17-balsam', 'slt17-begonia', 'slt17-j7', 'slt12-anemone', 'slt12-jasmine', 'slt28-palm', 'slt28-pine', 'slt11-rose', 'slt11-orchid', 'greatwall-a', 'greatwall-b', 'forge-lsys1', 'forge-lsys2', 'nonibert', 'lonibert', 'qiguo-2', 'qinguo-2', 'zhaoguo-2', 'weiguo-2', 'hanguo-2', 'chuguo-2', 'gw-minipdt-quincy1', 'gw-minipdt-quincy2', 'pdt-xian-2', 'pdt-xianyang-2', 'pdt-weinan-2', 'pdt-tongchuan-2', 'pdt-yanan-2', 'pdt-yulin-2', 'fig', 'yam', 'pdt-xian', 'pdt-xianyang', 'pdt-weinan', 'pdt-tongchuan', 'pdt-yanan', 'pdt-yulin', 'shanhai', 'yanmen', 'qiguo', 'qinguo', 'slt113-cavaliers', 'slt113-raptors', 'slt111-morphia', 'slt111-opium', 'slt103-cicada', 'slt103-cricket', 'slt103-j7', 'slt105-nongfu', 'slt105-shanquan', 'slt105-j7', 'slt112-warriors', 'slt112-spurs', 'sunshine', 'moonlight', 'guo', 'wan', 'pdt-winter', 'pdt-summer', 'ibmdow-reg1', 'ibmdow-reg2', 'pdt-lotus', 'pdt-reed', 'pdt-pepper', 'pdt-pumpkin', 'pdt-mars', 'pdt-mercury', 'pdt-earth', 'pdt-venus', 'calla', 'choko', 'pdt-jupiter', 'pdt-saturn', 'pdt-sparrow', 'pdt-swallow', 'pdt-magpie', 'pdt-phoenix', 'pdt-seagull', 'slt7-tulip', 'slt7-lilac']

#name_list=['pdt-honey', 'pdt-forge-natt', 'calla', 'slt112-onager', 'g07-31', 'qiguo', 'forge-pdt-10', 'pdt-yulin-2', 'pdt-pitaya', 'slt13-celery', 'qinguo', 'pdt-reed', 'pdt-summer', 'slt7-lilac', 'forge-pdt-11', 'ibmdow-reg2', 'slt60-loquat', 'slt17-balsam', 'f15-34', 'prose', 'pdt-gw11', 'pdt-weinan', 'slt105-shanquan', 'pdt-tongchuan-2', 'pdt-gw6', 'g07-28', 'pdt-jupiter', 'qinguo-2', 'slt17-begonia', 'slt11-orchid', 'yanmen', 'poetry', 'slt15-ginseng', 'slt104-grape', 'slt106-tmac', 'slt105-j7', 'pdt-waxberry', 'slt12-anemone', 'slt103-cicada', 'pdt-gw5', 'pdt-venus', 'slt113-raptors', 'shanhai', 'slt28-palm', 'pdt-orange', 'f13-34', 'pdt-mercury', 'slt60-j7', 'greatwall-b', 'g07-27', 'pdt-weinan-2', 'f15-36', 'slt102-mamba', 'fig', 'pdt-mars', 'pdt-yanan-2', 'slt60-cactus', 'greatwall-a', 'slt60-clove', 'pdt-mango', 'slt106-kb', 'pdt-tongchuan', 'slt112-warriors', 'slt15-medlar', 'zhaoguo-2', 'slt102-cobra', 'moonlight', 'kvm-dhcp', 'pdt-longan', 'yam', 'g07-29', 'pdt-sparrow', 'nonibert', 'slt7-tulip', 'forge-lsys1', 'slt102-python', 'gw-minipdt-quincy1', 'weiguo-2', 'slt11-rose', 'botree', 'slt103-cricket', 'pdt-lotus', 'pdt-seagull', 'slt111-opium', 'zinnia', 'pdt-xian-2', 'pdt-earth', 'pdt-magpie', 'pdt-peach', 'pdt-hulk', 'pdt-gw12', 'lonibert', 'attacking', 'f14-23', 'slt28-pine', 'slt123-north', 'slt113-cavaliers', 'slt123-pyke', 'paper', 'chuguo-2', 'pdt-melon', 'smily-vsrx', 'gw-minipdt-quincy2', 'pdt-pumpkin', 'slt17-j7', 'slt111-morphia', 'slt60-lemon', 'pdt-thor', 'pdt-phoenix', 'qiguo-2', 'f17-44', 'choko', 'pdt-yanan', 'slt112-pe', 'slt103-j7', 'slt106-ai', 'pdt-xianyang', 'slt104-orange', 'pdt-pepper', 'guo', 'pdt-berry', 'pdt-lemon', 'forge-lsys2', 'sunshine', 'slt123-wyk', 'pdt-coconut', 'slt13-carrot', 'slt12-jasmine', 'pdt-yulin', 'pdt-winter', 'pdt-casaba', 'peace', 'f13-33', 'pdt-swallow', 'slt102-adder', 'wan', 'pdt-xian', 'defending', 'pdt-xianyang-2', 'slt112-spurs', 'ibmdow-reg1', 'hanguo-2', 'pdt-saturn', 'smily-peer', 'slt123-wall', 'slt105-nongfu', 'honor-vsrx']
#name_list=['pdt-honey', 'calla', 'slt112-onager', 'g07-31', 'qiguo', 'pdt-yulin-2', 'pdt-pitaya', 'slt13-celery', 'qinguo', 'pdt-reed', 'pdt-summer', 'ibmdow-reg2', 'slt60-loquat', 'slt17-balsam', 'prose', 'pdt-gw11', 'pdt-weinan', 'slt105-shanquan', 'pdt-tongchuan-2', 'g07-28', 'qinguo-2', 'slt17-begonia', 'slt11-orchid', 'yanmen', 'poetry', 'slt15-ginseng', 'slt104-grape', 'slt106-tmac', 'slt105-j7', 'pdt-waxberry', 'slt12-anemone', 'slt103-cicada', 'pdt-venus', 'slt113-raptors', 'shanhai', 'slt28-palm', 'pdt-orange', 'pdt-mercury', 'slt60-j7', 'greatwall-b', 'g07-27', 'pdt-weinan-2', 'slt102-mamba', 'pdt-mars', 'pdt-yanan-2', 'greatwall-a', 'pdt-mango', 'slt106-kb', 'pdt-tongchuan', 'slt112-warriors', 'slt15-medlar', 'zhaoguo-2', 'slt102-cobra', 'moonlight', 'pdt-longan', 'g07-29', 'nonibert', 'forge-lsys1', 'slt102-python', 'gw-minipdt-quincy1', 'weiguo-2', 'slt11-rose', 'botree', 'slt103-cricket', 'pdt-lotus', 'slt111-opium', 'pdt-xian-2', 'pdt-earth', 'pdt-peach', 'pdt-gw12', 'lonibert', 'attacking', 'slt28-pine', 'slt123-north', 'slt113-cavaliers', 'slt123-pyke', 'paper', 'chuguo-2', 'pdt-melon', 'smily-vsrx', 'gw-minipdt-quincy2', 'pdt-pumpkin', 'slt17-j7', 'slt111-morphia', 'slt60-lemon', 'qiguo-2', 'f17-44', 'choko', 'pdt-yanan', 'slt112-pe', 'slt103-j7', 'slt106-ai', 'pdt-xianyang', 'slt104-orange', 'pdt-pepper', 'guo', 'pdt-berry', 'pdt-lemon', 'forge-lsys2', 'sunshine', 'slt123-wyk', 'pdt-coconut', 'slt13-carrot', 'slt12-jasmine', 'pdt-yulin', 'pdt-winter', 'pdt-casaba', 'peace', 'slt102-adder', 'wan', 'pdt-xian', 'defending', 'pdt-xianyang-2', 'slt112-spurs', 'ibmdow-reg1', 'hanguo-2', 'slt123-wall', 'slt105-nongfu', 'honor-vsrx']
#name_list=['gw-minipdt-quincy1','pdt-xian','pdt-tongchuan','slt28-palm','slt17-balsam','slt15-medlar','pdt-xian-2','pdt-tongchuan-2','slt11-orchid','pdt-honey','nonibert','slt104-orange','slt112-pe','poetry','botree','f17-44','slt112-onager','greatwall-a','qinguo-2','shanhai','pdt-melon','slt60-lemon','peace','pdt-pitaya','pdt-mango','pdt-peach']



device_owner_dict={'smily-peer':'ryanliu','slt7-tulip':'haliu','slt7-lilac':'haliu','slt14-cosmos':'darrenli','slt14-crocus':'darrenli','smily-vsrx':'ryanliu','slt17-j7':'darrenli','slt60-j7':'darrenli','slt60-lemon':'darrenli','slt60-loquat':'darrenli','pdt-coconut':'kchintada','pdt-longan':'kchintada','pdt-orange':'kchintada','poetry':'hparvathanen','peace':'hparvathanen','prose':'hparvathanen','paper':'hparvathanen','honor-vsrx': 'ryanliu','pdt-yanan': 'rvantari', 'g07-27': 'ryanliu', 'g07-29': 'ryanliu', 'g07-28': 'ryanliu', 'pdt-tongchuan': 'rvantari','slt123-wyk': 'ryanliu', 'slt123-pyke': 'ryanliu', 'pdt-xianyang': 'rvantari', 'pdt-gw12': 'arieszhan', 'slt112-spurs': 'emilydu', 'pdt-melon': 'kchintada', 'f13-33': 'darrenli', 'f13-34': 'darrenli', 'f15-34': 'darrenli', 'yanmen': 'udronamraju', 'slt105-shanquan': 'haliu', 'pdt-vsrx08': 'darrenli', 'fig': 'yangchen', 'pdt-vsrx04': 'darrenli', 'pdt-peach': 'rvantari', 'pdt-vsrx06': 'darrenli', 'pdt-vsrx07': 'darrenli', 'pdt-vsrx01': 'darrenli', 'pdt-vsrx02': 'darrenli', 'pdt-vsrx03': 'darrenli', 'slt28-palm': 'haliu', 'slt12-anemone': 'yangchen', 'pdt-lotus': 'haliu', 'pdt-weinan-2': 'arielwei', 'slt112-pe': 'crachakonda', 'pdt-hulk': 'darrenli', 'slt102-adder': 'ryanliu', 'pdt-xian-2': 'arielwei', 'qinguo': 'ztao', 'guo': 'deanchen', 'slt111-morphia': 'emilydu', 'pdt-sparrow': 'arielwei', 'pdt-honey': 'kchintada', 'pdt-tongchuan-2': 'arielwei', 'pdt-yanan-2': 'arielwei', 'forge-lsys1': 'ztao', 'forge-lsys2': 'ztao', 'gw-minipdt-quincy2': 'haliu', 'f17-44': 'crachakonda', 'gw-minipdt-quincy1': 'haliu', 'pdt-yulin-2': 'arielwei', 'pdt-jupiter': 'deanchen', 'slt113-raptors': 'emilydu', 'forge-pdt-10': 'ztao', 'forge-pdt-11': 'ztao', 'slt60-clove': 'yangchen', 'slt15-ginseng': 'darrenli', 'slt103-j7': 'deanchen', 'pdt-yulin': 'rvantari', 'pdt-venus': 'deanchen', 'pdt-gw6': 'ztao', 'pdt-gw5': 'ztao', 'slt102-python': 'ryanliu', 'slt112-onager': 'crachakonda', 'slt17-balsam': 'darrenli', 'choko': 'deanchen', 'botree': 'crachakonda', 'ibmdow-reg1': 'arieszhan', 'ibmdow-reg2': 'arieszhan', 'qiguo-2': 'crachakonda', 'Calla': 'deanchen', 'pdt-berry': 'rvantari', 'slt60-cactus': 'yangchen', 'slt104-orange': 'udronamraju', 'pdt-pepper': 'hparvathanen', 'slt111-opium': 'emilydu', 'pdt-weinan': 'rvantari', 'pdt-mango': 'rvantari', 'nonibert': 'kchintada', 'wan': 'deanchen', 'slt105-j7': 'haliu', 'yam': 'yangchen', 'pdt-orangepdt-coconutpdt-longan': 'kchintada', 'pdt-mercury': 'deanchen', 'f16-42': 'darrenli', 'slt123-wall': 'ryanliu', 'f16-40': 'darrenli', 'pdt-winter': 'emilydu', 'slt28-pine': 'haliu', 'pdt-vsrx09': 'darrenli', 'f14-23': 'darrenli', 'slt15-medlar': 'darrenli', 'sunshine': 'arieszhan', 'shanhai': 'udronamraju', 'pdt-vsrx05': 'darrenli', 'f15-36': 'darrenli', 'qinguo-2': 'crachakonda', 'pdt-gw11': 'arieszhan', 'slt13-celery': 'kchintada', 'greatwall-b': 'crachakonda', 'greatwall-a': 'crachakonda', 'zinnia': 'ryanliu', 'slt13-carrot': 'kchintada', 'slt103-cicada': 'deanchen', 'slt112-warriors': 'emilydu', 'slt106-tmac': 'ryanliu', 'pdt-earth': 'deanchen', 'slt105-nongfu': 'haliu', 'Prose': 'hparvathanen', 'slt12-jasmine': 'yangchen', 'kvm-dhcp': 'ryanliu', 'pdt-saturn': 'deanchen', 'pdt-reed': 'haliu', 'Peace': 'hparvathanen', 'pdt-casaba': 'rvantari', 'pdt-pitaya': 'rvantari', 'defending': 'arielwei', 'slt102-cobra': 'ryanliu', 'pdt-xianyang-2': 'arielwei', 'slt106-kb': 'ryanliu', 'Zinnia': 'deanchen', 'pdt-forge-natt': 'darrenli', 'pdt-mars': 'deanchen', 'lonibert': 'kchintada', 'slt123-north': 'ryanliu', 'pdt-phoenix': 'arielwei', 'pdt-magpie': 'arielwei', 'pdt-swallow': 'arielwei', 'pdt-summer': 'emilydu', 'g07-31': 'ryanliu', 'pdt-pumpkin': 'hparvathanen', 'pdt-seagull': 'arielwei', 'slt102-mamba': 'ryanliu', 'slt11-orchid': 'crachakonda', 'pdt-xian': 'rvantari', 'slt104-grape': 'udronamraju', 'pdt-waxberry': 'kchintada', 'slt103-cricket': 'deanchen', 'qiguo': 'ztao', 'slt106-ai': 'ryanliu', 'pdt-thor': 'darrenli', 'pdt-lemon': 'rvantari', 'attacking': 'arielwei', 'moonlight': 'arieszhan', 'calla': 'deanchen', 'slt113-cavaliers': 'emilydu', 'slt17-begonia': 'darrenli', 'slt11-rose': 'crachakonda','chuguo-2': 'crachakonda','weiguo-2': 'crachakonda','zhaoguo-2': 'crachakonda','hanguo-2': 'crachakonda'}

def get_date_list(interval):
    date_list=[]
    for i in range(interval):
        delta=datetime.timedelta(days=i)
        #now=datetime.datetime.now()
        #today=datetime.date(now.year,now.month,now.day)  
        now=datetime.datetime(2019, 5, 27, 23, 59, 59, 36867)
        today=datetime.date(now.year,now.month,now.day)  
        if (today-delta).timetuple()[1]<10:
            month=('0%s' % (today-delta).timetuple()[1])
        else:
            month=('%s' % (today-delta).timetuple()[1])
        if (today-delta).timetuple()[2]<10:
            day=('0%s' % (today-delta).timetuple()[2])
        else:
            day=('%s' % (today-delta).timetuple()[2])
        date_list.append('%s-%s-%s' % ((today-delta).timetuple()[0],month,day))
    return date_list

def get_error_testbed_list(df_error,name_list):
    error_testbed_list=[]
    
    for item in name_list:
        error_session_list=df_error.loc[df_error['name']==item]['session'].tolist()
        error_ha_list=df_error.loc[df_error['name']==item]['HA'].tolist()
        error_fpc_list=df_error.loc[df_error['name']==item]['fpc'].tolist()
        iter_session_list=[]
        for k,v in itertools.groupby(error_session_list):
            iter_session_list.append(list(v))
        zero_session_list=[]
        for session_item in iter_session_list:
            if 0 in session_item:
                zero_session_list.append(len(session_item))
        
        iter_ha_list=[]
        for k,v in itertools.groupby(error_ha_list):
            iter_ha_list.append(list(v))
        zero_ha_list=[]
        for ha_item in iter_ha_list:
            if 0 in ha_item:
                zero_ha_list.append(len(ha_item))
        
        iter_fpc_list=[]
        for k,v in itertools.groupby(error_fpc_list):
            iter_fpc_list.append(list(v))
        zero_fpc_list=[]
        for fpc_item in iter_fpc_list:
            if 0 in fpc_item:
                zero_fpc_list.append(len(fpc_item))
        
        if len(zero_session_list)!=0:
            if max(zero_session_list)>=16:
                if item not in error_testbed_list:
                    error_testbed_list.append(item)
        if len(zero_ha_list)!=0:
            if max(zero_ha_list)!=len(error_ha_list):
                if max(zero_ha_list)>=16:
                    if item not in error_testbed_list:
                        error_testbed_list.append(item)
        if len(zero_fpc_list)!=0:
            if max(zero_fpc_list)>=16:
                if item not in error_testbed_list:
                    error_testbed_list.append(item)
                    
        if len(zero_session_list)>=12 or len(zero_ha_list)>=12 or len(zero_fpc_list)>=12:
            if item not in error_testbed_list:
                error_testbed_list.append(item)
    return error_testbed_list

def write_html(start_date,year_start,end_date,year_end,device_name_dict,name_list,cnrd_owner_dict,tcs_owner_dict):
    #name_list=glob.glob('*session.png')
    name_list.sort()
    if platform.system()=='Linux':
        directory="/var/www/html/log"
    else:
        directory="/Users/ryanliu/Downloads/Ansible/facts"
    htmlfile=open('%s/index.html' % directory, 'w')
    htmlfile.write("""<html><body><head><title>PDT Testbeds Status</title>
    </head>
    <center>""")
    htmlfile.write("""<h1><font size="5" face="verdana" color="#1f77b4">PDT Testbeds Status (%s/%s to %s/%s)</font></h1>""" % (start_date,year_start,end_date,year_end))
    htmlfile.write("""<p style="text-align: center;">""")
    for key, value in device_name_dict.items():
        if key!='All' and key!='Error' and key!='CNRD' and key!='TCS':
            htmlfile.write("""<a href="http://10.208.176.205/log/%s_status.html"><font size="4" face="arial" color="#1f77b4">%s Testbeds (%s)</font></a>""" % (key,key,len(value)))
            htmlfile.write('&nbsp;&nbsp;')
            htmlfile.write('\n')
    htmlfile.write("""<a href="http://10.208.176.205/log/tcs_testbeds.html"><font size="4" face="arial" color="#1f77b4">TCS Testbeds (%s)</font></a>""" % len(device_name_dict['TCS']))  
    htmlfile.write('&nbsp;&nbsp;')
    htmlfile.write('\n')
    htmlfile.write("""<a href="http://10.208.176.205/log/cnrd_testbeds.html"><font size="4" face="arial" color="#1f77b4">CNRD Testbeds (%s)</font></a>""" % len(device_name_dict['CNRD']))  
    htmlfile.write("""</p>""")
    htmlfile.write("""<a href="http://10.208.176.205/log/All_status.html"><font size="4" face="arial" color="#1f77b4">All Testbeds (%s)</font></a>""" % len(device_name_dict['All']))  
    htmlfile.write("""</p>""")
    htmlfile.write("""<p style="text-align: center;">""")
    htmlfile.write("""<a href="http://10.208.176.205/log/session-ha-fpc_log.csv"><font size="4" face="arial" color="#1f77b4">Download Log File for Detailed Info</font></a>""")  
    htmlfile.write('&nbsp;&nbsp;')
    htmlfile.write('\n')
    htmlfile.write("""<a href="http://10.208.176.205/log/Error_status.html"><font size="4" face="arial" color="#1f77b4">Testbeds with Error State (%s)</font></a>""" % len(device_name_dict['Error']))  
    htmlfile.write("""</p>""")
    for item in name_list:
        htmlfile.write("""<a href="http://10.208.176.205/log/%s.html"><img src="%s_version.png" width="600" height="320" /></a>""" % (item.split('_')[0],item.split('_')[0]))
    htmlfile.write("""</center></body>
    </html>""")
    htmlfile.close()

    htmlfile=open('%s/cnrd_testbeds.html' % directory, 'w')
    htmlfile.write("""<html><body><head><title>CNRD Testbeds Status</title>
    </head>
    <center>""")
    htmlfile.write("""<h1><font size="5" face="verdana" color="#1f77b4">CNRD Testbeds Status (%s/%s to %s/%s)</font></h1>""" % (start_date,year_start,end_date,year_end))
    htmlfile.write("""<p style="text-align: center;">""")
    i=1
    for key, value in cnrd_owner_dict.items():
        if i==4 or i==7:
            htmlfile.write("""</p>""")
            htmlfile.write("""<p style="text-align: center;">""")
        htmlfile.write("""<a href="http://10.208.176.205/log/%s_status.html"><font size="4" face="arial" color="#1f77b4">%s's Testbeds (%s)</font></a>""" % (key,key,len(value)))
        htmlfile.write('&nbsp;&nbsp;')
        htmlfile.write('\n')
        i=i+1
    htmlfile.write("""</p>""")
    for key, value in cnrd_owner_dict.items():
        htmlfile.write("""<p><font size="5" face="verdana" color="black">%s's Testbeds</font></p>""" % key)
        htmlfile.write("""<a href="http://10.208.176.205/log/%s_status.html"><img src="%s_version.png" width="600" height="320" /></a>""" % (key,value[0]))
    htmlfile.write("""</center></body>
    </html>""")
    htmlfile.close()

    htmlfile=open('%s/tcs_testbeds.html' % directory, 'w')
    htmlfile.write("""<html><body><head><title>TCS Testbeds Status</title>
    </head>
    <center>""")
    htmlfile.write("""<h1><font size="5" face="verdana" color="#1f77b4">TCS Testbeds Status (%s/%s to %s/%s)</font></h1>""" % (start_date,year_start,end_date,year_end))
    htmlfile.write("""<p style="text-align: center;">""")
    i=1
    for key, value in tcs_owner_dict.items():
        if i==4:
            htmlfile.write("""</p>""")
            htmlfile.write("""<p style="text-align: center;">""")
        htmlfile.write("""<a href="http://10.208.176.205/log/%s_status.html"><font size="4" face="arial" color="#1f77b4">%s's Testbeds (%s)</font></a>""" % (key,key,len(value)))
        htmlfile.write('&nbsp;&nbsp;')
        htmlfile.write('\n')
        i=i+1
    htmlfile.write("""</p>""")
    for key, value in tcs_owner_dict.items():
        htmlfile.write("""<p><font size="5" face="verdana" color="black">%s's Testbeds</font></p>""" % key)
        htmlfile.write("""<a href="http://10.208.176.205/log/%s_status.html"><img src="%s_version.png" width="600" height="320" /></a>""" % (key,value[0]))
    htmlfile.write("""</center></body>
    </html>""")
    htmlfile.close()

    for item in name_list:
        htmlfile=open('%s/%s.html' % (directory,item.split('_')[0]), 'w')
        htmlfile.write("""<html><body><head><title>PDT Testbeds Status</title>
        </head>
        <center>""")
        htmlfile.write("""<h1><font size="4" face="verdana">%s Up Time with Version Info and System Status (%s/%s to %s/%s)</font></h1>""" % (item.split('_')[0],start_date,year_start,end_date,year_end))
        
        htmlfile.write("""<img src="%s_session.png" width="2400" height="800" /><br>""" % item)
        
        htmlfile.write("""
        <p><font size="3" face="arial" color="blue">Blue Line </font>
        <font size="3" face="arial" color="black">(Total Sessions Number),</font>
        <font size="3" face="arial" color="green">Green Line </font>
        <font size="3" face="arial" color="black">(HA Status:Pass=1,Fail=0),</font>
        <font size="3" face="arial" color="red">Red Line </font>
        <font size="3" face="arial" color="black">(PIC Status:Pass=2,Fail=0)</font>
        </p>
        """)
        htmlfile.write("""</center></body>
        </html>""")
        htmlfile.close()

    htmlfile=open('%s/status.html' % directory, 'w')
    htmlfile.write("""<html><body><head><title>PDT Testbeds Status</title>
    </head>""")
    htmlfile.write("""
    <center>
    <h1><font size="5" face="verdana">PDT Testbeds Status with Version Info (%s/%s to %s/%s)</font></h1>
    <p><font size="4" face="arial" color="blue">Blue Line </font>
    <font size="4" face="arial" color="black">(Total Sessions Number),</font>
    <font size="4" face="arial" color="green">Green Line </font>
    <font size="4" face="arial" color="black">(HA Status:Pass=1,Fail=0),</font>
    <font size="4" face="arial" color="red">Red Line </font>
    <font size="4" face="arial" color="black">(PIC Status:Pass=2,Fail=0)</font>
    </p>
    """ % (start_date,year_start,end_date,year_end))
    for item in name_list:
        htmlfile.write("""<p><font size="5" face="verdana" color="black">%s</font></p>""" % item.split('_')[0])
        htmlfile.write("""<img src="%s_status.png" width="1600" height="400" />""" % item.split('_')[0])
    htmlfile.write("""</center></body>
    </html>""")
    htmlfile.close()
    
    for key, value in device_name_dict.items():
        htmlfile=open('%s/%s_status.html' % (directory,key), 'w')
        htmlfile.write("""<html><body><head><title>PDT Testbeds Status</title>
        </head>""")
        htmlfile.write("""
        <center>
        <h1><font size="5" face="verdana">%s Testbeds Status with Version Info (%s/%s to %s/%s)</font></h1>
        <p><font size="4" face="arial" color="blue">Blue Line </font>
        <font size="4" face="arial" color="black">(Total Sessions Number),</font>
        <font size="4" face="arial" color="green">Green Line </font>
        <font size="4" face="arial" color="black">(HA Status:Pass=1,Fail=0),</font>
        <font size="4" face="arial" color="red">Red Line </font>
        <font size="4" face="arial" color="black">(PIC Status:Pass=2,Fail=0)</font>
        </p>
        """ % (key,start_date,year_start,end_date,year_end))
        #if key=='TCS':
        value.sort()
        for item in value:
            htmlfile.write("""<p><font size="5" face="verdana" color="black">%s (Owner:%s)</font></p>""" % (item.split('_')[0],device_owner_dict['%s' % item.split('_')[0]]))
            htmlfile.write("""<img src="%s_status.png" width="1600" height="400" />""" % item.split('_')[0])
        #else:
        #    value.sort()
        #    for item in value:
        #        htmlfile.write("""<p><font size="5" face="verdana" color="black">%s</font></p>""" % item.split('_')[0])
        #        htmlfile.write("""<img src="%s_status.png" width="1600" height="400" />""" % item.split('_')[0])
        htmlfile.write("""</center></body>
        </html>""")
        htmlfile.close()
    for key, value in cnrd_owner_dict.items():
        htmlfile=open('%s/%s_status.html' % (directory,key), 'w')
        htmlfile.write("""<html><body><head><title>PDT Testbeds Status</title>
        </head>""")
        htmlfile.write("""
        <center>
        <h1><font size="5" face="verdana">%s Testbeds Status with Version Info (%s/%s to %s/%s)</font></h1>
        <p><font size="4" face="arial" color="blue">Blue Line </font>
        <font size="4" face="arial" color="black">(Total Sessions Number),</font>
        <font size="4" face="arial" color="green">Green Line </font>
        <font size="4" face="arial" color="black">(HA Status:Pass=1,Fail=0),</font>
        <font size="4" face="arial" color="red">Red Line </font>
        <font size="4" face="arial" color="black">(PIC Status:Pass=2,Fail=0)</font>
        </p>
        """ % (key,start_date,year_start,end_date,year_end))
        value.sort()
        for item in value:
            htmlfile.write("""<p><font size="5" face="verdana" color="black">%s (Owner:%s)</font></p>""" % (item,key))
            htmlfile.write("""<img src="%s_status.png" width="1600" height="400" />""" % item)
        htmlfile.write("""</center></body>
        </html>""")
        htmlfile.close()
    for key, value in tcs_owner_dict.items():
        htmlfile=open('%s/%s_status.html' % (directory,key), 'w')
        htmlfile.write("""<html><body><head><title>PDT Testbeds Status</title>
        </head>""")
        htmlfile.write("""
        <center>
        <h1><font size="5" face="verdana">%s Testbeds Status with Version Info (%s/%s to %s/%s)</font></h1>
        <p><font size="4" face="arial" color="blue">Blue Line </font>
        <font size="4" face="arial" color="black">(Total Sessions Number),</font>
        <font size="4" face="arial" color="green">Green Line </font>
        <font size="4" face="arial" color="black">(HA Status:Pass=1,Fail=0),</font>
        <font size="4" face="arial" color="red">Red Line </font>
        <font size="4" face="arial" color="black">(PIC Status:Pass=2,Fail=0)</font>
        </p>
        """ % (key,start_date,year_start,end_date,year_end))
        value.sort()
        for item in value:
            htmlfile.write("""<p><font size="5" face="verdana" color="black">%s (Owner:%s)</font></p>""" % (item,key))
            htmlfile.write("""<img src="%s_status.png" width="1600" height="400" />""" % item)
        htmlfile.write("""</center></body>
        </html>""")
        htmlfile.close()
def write_version_csv(df,name_list):       
    df.drop(['type','session','HA','fpc','time'],axis=1,inplace=True)
    df=df.drop_duplicates()
    #print df.loc[df['name']=='nonibert']
    df1=df.groupby(["name"]).apply(lambda x: x.sort_values(["booted_time"], ascending=True)).reset_index(drop=True)
    #print df1.loc[df1['name']=='nonibert']

    for i in range(len(df1['name'])):
        value1=df1['booted_time'][i]
        timelist=[int(value1.split(' ')[0].split('-')[0]),int(value1.split(' ')[0].split('-')[1]),int(value1.split(' ')[0].split('-')[2]),int(value1.split(' ')[1].split(':')[0]),int(value1.split(' ')[1].split(':')[1]),int(value1.split(' ')[1].split(':')[2]),0,0,0]
        df1['booted_time'][i]=time.mktime(timelist)
    #print df1
    frame_list=[]
    #name_list=list(set(df1['name']))
    #name_list=['slt60-lemon','slt123-wyk','g07-29','slt106-kb','slt102-python','slt15-medlar','slt17-balsam','slt12-jasmine','slt28-palm','slt11-rose','nonibert','qiguo-2','gw-minipdt-quincy1','pdt-xian','pdt-tongchuan']
    #name_list=['qinguo-2','nonibert','gw-minipdt-quincy1','pdt-xian','pdt-tongchuan','slt28-palm','slt17-balsam']
    #name_list=['slt28-palm']
    #name_list=['nonibert']
    ##start_time=time.mktime([2019,3,18,0,0,0,0,0,0])
    ##now=datetime.datetime.now()
    ##end_time=time.mktime([now.year,now.month,now.day,now.hour,now.minute,now.second,0,0,0])
    #end_time=time.mktime([2019,3,21,14,20,0,0,0,0])
    version_list_dict={}
    
    for item in name_list:
        current_date=0
        current_time=0
        df_time_item=df_time.loc[df_time['name']==item]
        df_time_item=df_time_item.reset_index(drop=True)
        start_time_list=df_time_item['time'][0].split(',')
        for start_time_item in start_time_list:
            if "Current time" in start_time_item:
                begin_date=start_time_item.split()[2]
                begin_time=start_time_item.split()[3]
        current_time_list=df_time_item['time'][len(df_time_item['time'])-1].split(',')
        for current_time_item in current_time_list:
            if "Current time" in current_time_item:
                current_date=current_time_item.split()[2]
                current_time=current_time_item.split()[3]
        if '-' in begin_date and ':' in begin_time:
            start_time=time.mktime([int(begin_date.split('-')[0]),int(begin_date.split('-')[1]),int(begin_date.split('-')[2]),int(begin_time.split(':')[0]),int(begin_time.split(':')[1]),int(begin_time.split(':')[2]),0,0,0])
        else:
            start_time=time.mktime([int(date_list[-1].split('-')[0]),int(date_list[-1].split('-')[1]),int(date_list[-1].split('-')[2]),0,0,0,0,0,0])
        if '-' in current_date and ':' in current_time:
            end_time=time.mktime([int(current_date.split('-')[0]),int(current_date.split('-')[1]),int(current_date.split('-')[2]),int(current_time.split(':')[0]),int(current_time.split(':')[1]),int(current_time.split(':')[2]),0,0,0])
        else:
            #now=datetime.datetime.now()
            #end_time=time.mktime([now.year,now.month,now.day,now.hour,now.minute,now.second,0,0,0])
            now=datetime.datetime(2019, 5, 27, 23, 59, 59, 36867)
            end_time=time.mktime([now.year,now.month,now.day,now.hour,now.minute,now.second,0,0,0])
        version_list_init=[]
        df2=df1.loc[df1['name']==item]
        df2=df2.reset_index(drop=True)
        #df2_before=df2.loc[df2['booted_time']<start_time]
        #df2_after=df2.loc[df2['booted_time']>=start_time]
        #if df2_before.empty!=True:
        #    df2=pd.concat([df2_before.iloc[-1:],df2_after])
        #    df2=df2.reset_index(drop=True)
        for version_list_item in df2['version']:
            if version_list_item not in version_list_init:
                version_list_init.append(version_list_item)
        version_list_dict['%s' % item]=version_list_init
        for i in range(len(df2['name'])):
            if len(df2['name'])-1==0:
                if df2['booted_time'][i]<start_time:
                    interval=(end_time-start_time)/3600
                else:
                    interval=(end_time-df2['time'][i])/3600
                df2['booted_time'][i]=round(interval,1)
            else:
                if i==0:
                    if df2['booted_time'][i]<start_time:
                        interval=(df2['booted_time'][i+1]-start_time)/3600
                    else:
                        interval=(df2['booted_time'][i+1]-df2['booted_time'][i])/3600
                elif i==len(df2['name'])-1:
                    interval=(end_time-df2['booted_time'][i])/3600
                else:
                    interval=(df2['booted_time'][i+1]-df2['booted_time'][i])/3600
                df2['booted_time'][i]=round(interval,1)
        df2=df2.groupby(['version'], sort=False).sum()
        frame_list.append(df2)
        #print df2.index[0]

    #dict_list=[]
    #for item in frame_list:
    #    dict={}
    #    for i in range(len(item.index)):
    #        #dict['%s_%s' % (item['version'][i],i)]=[item['time'][i]]
    #        dict['%s' % item.index[i]]=[item['time'][i]]
    #    dict_list.append(dict)

    DataFrame_list=[]
    cols=[]
    i=0

    for item in frame_list:
        item_list=[]
        columns_list=[]
        for num in range(len(item.index)):
            item_list.append(item['booted_time'][num])
            columns_list.append(item.index[num])
            num=num+1
    
        frame=pd.DataFrame(item_list,index=columns_list, columns=['%s' % name_list[i]])
        frame=frame.T
        check_num=0
        sequence_list=[]
        sequence=0
        for item in list(frame):
            if item in cols:
                check_num=check_num+1
            else:
                sequence_list.append(sequence)
            sequence=sequence+1
        if check_num!=0:
            sequence_num1=0
            sequence_num2=0
            for item in list(frame):
                if sequence_num1 in sequence_list:
                    cols.insert(sequence_num2,item)
                    sequence_num2=sequence_num2+1
                sequence_num1=sequence_num1+1
        else:
            cols=cols+list(frame)
        DataFrame_list.append(frame)
        i=i+1
    DataFrame=pd.concat(DataFrame_list,axis=0,sort=False).fillna(0)
    DataFrame=DataFrame.loc[:,sorted(set(cols),key=cols.index)]
    DataFrame.to_csv('log/version_info.csv')
    return version_list_dict

#DataFrame_list=[]
#i=0
#for item in dict_list:
#    frame=pd.DataFrame(item,index=['%s' % name_list[i]])
#    DataFrame_list.append(frame)
#    i=i+1
#DataFrame=pd.concat(DataFrame_list,axis=0,sort=False).fillna(0)

#device_name='nonibert'


def write_ha_csv(df1):
    for i in range(len(df1['name'])):
        if 'error' in df1['HA'][i]:
            df1['HA'][i]=0
            #df1.drop(index=i,inplace=True)
    df1.reset_index(drop=True, inplace=True)

    df1.to_csv('log/ha_info_init.csv')
    

def write_session_csv(df1):
    for i in range(len(df1['name'])):
        if type(df1['session'][i]) is float:
            df1['session'][i]=0
            #df1.drop(index=i,inplace=True)
        if type(df1['HA'][i]) is float:
            df1['HA'][i]=0
        if type(df1['fpc'][i]) is float:
            df1['fpc'][i]=0
        #if 'error' in df1['session'][i]:
        #    df1['session'][i]=0
        #if 'error' in df1['HA'][i]:
        #    df1['HA'][i]=0
        #if 'error' in df1['fpc'][i]:
        #    df1['fpc'][i]=0
    df1.reset_index(drop=True, inplace=True)

    df1.to_csv('log/session-ha-fpc_info_init.csv')
    i=0
    #print len(df1['session'])
    for item in df1['session']:
        if item!=0:
            if 'error' not in item:
                if 'node' in item:
                    if 'Total Sessions' in item:
                        if len(item.split('Total Sessions'))-1==2:
                            last_line1=item.split(',')[len(item.split(','))/2-1]
                            if 'Total Sessions' in last_line1:
                                df1['session'][i]=last_line1.split()[2]
                            else:
                                df1['session'][i]=0
                        else:
                            last_line1=item.split(',')[-1]
            
                            if last_line1.split()[2]=='reset' or last_line1.split()[2]=='failed':
                                #print item.split(',')
                                df1['session'][i]=0
                            else:   
                                df1['session'][i]=last_line1.split()[2]
                    elif 'Flow session' in item:
                        if len(item.split('node'))-1==2:
                            if len(item.split(','))%2==0:
                                last_line1=item.split(',')[len(item.split(','))/2-1]
                                if len(last_line1.split())>5:
                                    if last_line1.split()[5]=='to' or last_line1.split()[5]=='out':
                                        #print item.split(',')
                                        df1['session'][i]=0
                                    else:
                                        df1['session'][i]=last_line1.split()[5]
                                else:
                                    df1['session'][i]=0
                            else:
                                last_line1=item.split(',')[5]
                                if len(last_line1.split())>5:
                                    if last_line1.split()[5]=='to' or last_line1.split()[5]=='out':
                                        #print item.split(',')
                                        df1['session'][i]=0
                                    else:
                                        df1['session'][i]=last_line1.split()[5]
                                else:
                                    df1['session'][i]=0
                        else:
                            last_line1=item.split(',')[-1]
                            if len(last_line1.split())>5:
                                if last_line1.split()[5]=='to' or last_line1.split()[5]=='out':
                                    #print item.split(',')
                                    df1['session'][i]=0
                                else:
                                    df1['session'][i]=last_line1.split()[5]
                            else:
                                df1['session'][i]=0
                    else:
                        df1['session'][i]=0
                elif 'Total Sessions' in item:
                    last_line1=item.split(',')[-1]
                    if len(last_line1.split())>7:
                        df1['session'][i]=0
                    else:    
                        df1['session'][i]=last_line1.split()[2]
                elif 'Flow session' in item:
                    last_line2=item.split(',')[-1]
                    if len(last_line2.split())>5:
                        if last_line2.split()[5]=='to' or last_line2.split()[5]=='out':
                            #print item.split(',')
                            df1['session'][i]=0
                        else:
                            df1['session'][i]=last_line2.split()[5]
                    else:
                        df1['session'][i]=0
        
                else:
                    df1['session'][i]=0
            else:
                df1['session'][i]=0
        i=i+1
    #print len(df1['session'])
    i=0
    for ha_item in df1['HA']:
        
        if ha_item!=0:
            if 'error' not in ha_item:
                ha_item_list=ha_item.split(',')
                #print ha_item
                status_counter=0
                for status_item in ha_item_list:
                    #print status_item
                    if 'node' in status_item.split()[0]:
                        #print status_item.split()[1]
                        #print status_item.split()[5]
                        if status_item.split()[1]=='0':
                            status_counter+=1
                        if status_item.split()[2]=='disabled':
                            status_counter+=1
                        if status_item.split()[2]=='ineligible':
                            status_counter+=1
                        if status_item.split()[5]!='None':
                            status_counter+=1
                #print status_counter
                if status_counter==0:
                    df1['HA'][i]=1
                else:
                    df1['HA'][i]=0
            else:
                df1['HA'][i]=0
        
        i+=1
    i=0
    for fpc_item in df1['fpc']:
        
        if fpc_item!=0:
            if 'error' not in fpc_item:
                if fpc_item!='':
                    fpc_item_list=fpc_item.split(',')
                    #print fpc_item
                    fpc_status_counter=0
                    for fpc_status_item in fpc_item_list:
                        #print fpc_status_item
                        if 'Offline' in fpc_status_item:
                            #print fpc_status_item
                
                            if ('12x 10GE' not in fpc_status_item) and ('3x 40GE' not in fpc_status_item):
                    
                                fpc_status_counter+=1
                        if 'Present' in fpc_status_item:
                            fpc_status_counter+=1
                    #print status_counter
                    if fpc_status_counter==0:
                        df1['fpc'][i]=2
                    else:
                        df1['fpc'][i]=0
                else:
                    df1['fpc'][i]=0
            else:
                df1['fpc'][i]=0
        
        i+=1
    df1.to_csv('log/session-ha-fpc_info.csv')

def write_log_csv(df_log1,df_log2,df_log3):
    df_log1.rename({"time":"show system uptime"}, axis="columns", inplace=True)
    df_log1.drop(['name','version','booted_time','type','session','HA','fpc'],axis=1, inplace=True)
    df_log2.rename({"Unnamed: 0":"index","name":"Device name","version":"Version","session":"Total sessions","HA":"HA Status","fpc":"PIC Status"}, axis="columns", inplace=True)
    df_log2.drop(["index"], axis=1, inplace=True)
    df_log3.rename({"Unnamed: 0":"index","session":"show security monitoring","HA":"show chassis cluster status","fpc":"show chassis fpc pic-status"}, axis="columns", inplace=True)
    df_log3.drop(["index","name","version"], axis=1, inplace=True)
    result = pd.concat([df_log2, df_log3, df_log1], axis=1)
    if platform.system()=='Linux':
        result.to_csv('/var/www/html/log/session-ha-fpc_log.csv')
    else:
        df1.to_csv('session-ha-fpc_log.csv')
    
def bar_chart(version_list_bar,uptime_list,device_name,start_date,year_start,end_date,year_end):
    #version_list_bar.reverse()
    #uptime_list.reverse()
    x=version_list_bar
    y=np.array(uptime_list)
    #ax = plt.gca() 
    #ax.spines['right'].set_color('none') 
    #ax.spines['top'].set_color('none')
    #plt.figure(figsize=(30,8))
    fig = plt.figure(figsize=(36, 12))
    ax1 = fig.add_subplot(1,1,1)
    ax1.barh(x, y, color='#66CCCC', label='Up Time')
    for a,b in zip(x,y):
        ax1.text(b+0.08, a, '%.1f' % b, ha='left', va= 'bottom',fontsize=12)
    #fig, ax = plt.subplots()
    #ax.bar(x, y, color='#0066FF', label='Up Time')
    #for a,b in zip(x,y):
    #    ax1.text(a, b+0.05, '%.1f' % b, ha='center', va= 'bottom',fontsize=12)
    #plt.xticks(x,version_list_bar,rotation=15)
    ##plt.title('%s' % (device_name),ha='center', va= 'baseline',fontsize=120,color='#1f77b4')
    plt.title('%s' % (device_name),ha='center', va= 'baseline',fontsize=120,color='#66CCCC')
    #plt.title('%s Up Time with Version Info and System Status (%s/%s to %s/%s)' % (device_name,start_date,year_start,end_date,year_end),fontsize=30)
    #plt.xlabel('Version')
    plt.xlabel('Up Time (Hours)',fontsize=16)
    #plt.xlabel('%s' % device_name, ha='center', va= 'bottom',fontsize=20)
    #fig.autofmt_xdate()
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    plt.tight_layout()
    if platform.system()=='Linux':
        plt.savefig("/var/www/html/log/%s_version.png" % device_name, dpi=200, transparent=True, pad_inches = 0)
    else:
        plt.savefig("%s_version.png" % device_name, dpi=200, transparent=True, pad_inches = 0)
    plt.close(fig)
def bar_line_chart(x,y1,y2,y3,version_list,device_name,version_labels,time_values,version_list_short,uptime_list,start_date,year_start,end_date,year_end,version_middle_index_list):
    #fig,(ax1,ax2)=plt.subplots(1,2,figsize=(32,8))
    #plt.figure(figsize=(32,12))
    fig = plt.figure(figsize=(36, 12))
    #plt.figure(1)
    #ax1=plt.subplot(211)
    
    #plt.subplot(3,1,1)
    ax1 = fig.add_subplot(2,1,1)
    
    x1=version_list_bar
    y=np.array(uptime_list)
    #ax = plt.gca() 
    #ax.spines['right'].set_color('none') 
    #ax.spines['top'].set_color('none')
    #plt.figure(figsize=(30,8))
    ax1.barh(x1, y, color='#66CCCC', label='Up Time')
    #fig, ax = plt.subplots()
    #ax.bar(x, y, color='#0066FF', label='Up Time')
    for a,b in zip(x1,y):
        ax1.text(b+0.08, a, '%.1f' % b, ha='left', va= 'center',fontsize=12)
    plt.yticks(fontsize=12)
    #plt.xticks(x1,version_list_short,rotation=15,fontsize=12)
    #plt.title('%s Up Time with Version Info and System Status (%s/%s to %s/%s)' % (device_name,start_date,year_start,end_date,year_end),fontsize=18)
    #plt.xlabel('Version')
    plt.xlabel('Up Time (Hours)')
    #fig.autofmt_xdate()
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    #ax1.tick_params(axis='y', fontsize=15)
    #ax1.set_yticklabels(y_ticks, rotation=0, fontsize=15)
    plt.tight_layout()
    
    #plt.subplot(2,1,2)
    ax2 = fig.add_subplot(2,1,2)
    #ax.plot(x,y,color='#0066FF',label='Total Sessions')
    #ax = plt.gca() 
    #ax.xaxis.set_ticks_position('bottom')   
    #ax.yaxis.set_ticks_position('left')
    #ax.spines['bottom'].set_position(('data', 0))
    #ax.spines['left'].set_position(('data', 0))
    #row_colors=['green']
    #row_labels=['Time']
    #version_time_table=plt.table(cellText=time_values, colWidth=[0.1], rowLabels=version_labels, collLabels=version_labels, rowColours=row_colors, colColours=row_colors, loc='best')
    #print version_labels
    #print time_values
    #ax2.axis('off')
    
    #my_table.scale(2,2)
    
    ax2.plot(x,y1,color='blue',label='Total Sessions')
    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    #plt.title('Blue Line (Total Sessions Number), Green Line (HA Status:Pass=1,Fail=0), Red Line (PIC Status:Pass=2,Fail=0)', fontsize=18, y=1.15)
    #y_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)
    #ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    #ax2.get_yaxis().get_major_formatter().set_useOffset(False)
    #ax2.yaxis.set_major_formatter(y_formatter)
    plt.ylim(ymin=0)
    plt.xlim(xmin=0,xmax=len(x))
    #plt.xticks(x,version_list,rotation=270,fontsize=12)
    plt.xticks(x,version_list,rotation=270,fontsize=12)
    #plt.xticks(x,version_middle_index_list,rotation=45,fontsize=12)
    #plt.xlabel('Blue Line (Total Sessions Number), Green Line (HA Status:Pass=1,Fail=0), Red Line (PIC Status:Pass=2,Fail=0)',fontsize=18)
    plt.ylabel('Total Sessions Number',fontsize=16,labelpad=15)
    plt.grid()
    plt.tight_layout()
    plt.twinx()
    plt.plot(x,y2,color='green',label='HA Status')
    plt.plot(x,y3,color='red',label='FPC Status')
    plt.ylim(ymin=0)
    plt.ylabel('HA and PIC Status',rotation=270,fontsize=16,labelpad=15)
    
    ha_y_ticks = np.arange(0, 3, 1)
    plt.yticks(ha_y_ticks)
    plt.twiny()
    plt.xlim(xmin=0,xmax=len(x))
    #plt.xticks(x,version_middle_index_list,rotation=0,fontsize=12)
    #plt.xticks(x,version_list,rotation=270,fontsize=12)
    plt.xticks(x,version_middle_index_list,rotation=0,fontsize=12)
    #plt.xlabel('Blue Line (Total Sessions Number), Green Line (HA Status:Pass=1,Fail=0), Red Line (PIC Status:Pass=2,Fail=0)',fontsize=18)
    #plt.title('Total Sessions of Device (%s)' % device_name)
    #plt.xlabel('Version')
    #plt.ylabel('System Status (Pass=3, Fail=0,1,2)',rotation=270,fontsize=12,labelpad=15)
    #plt.twiny()
    #plt.xticks(x,version_middle_index_list,rotation=0,fontsize=12)
    #plt.grid()
    #fig.autofmt_xdate()
    #ax2 = plt.gca()
    #ax2.get_yaxis().get_major_formatter().set_useOffset(False)
    ax2.get_yaxis().get_major_formatter().set_scientific(False)
    ax2.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.tight_layout()
    #ax2=plt.subplot(211)
    if platform.system()=='Linux':
        plt.savefig("/var/www/html/log/%s_session.png" % device_name, dpi=200, transparent=True, pad_inches = 0)
    else:
        plt.savefig("%s_session.png" % device_name, dpi=200, transparent=True, pad_inches = 0)
    plt.close(fig)
def status_line_chart(x,y1,y2,y3,version_list,device_name,start_date,year_start,end_date,year_end,version_middle_index_list):
    fig = plt.figure(figsize=(36, 12))
    ##plt.figure(figsize=(32,8))
    ax1 = fig.add_subplot(1,1,1)
    ax1.plot(x,y1,color='blue',label='Total Sessions')
    ##plt.plot(x,y1,color='blue',label='Total Sessions')
    #plt.title('%s' % device_name,fontsize=20,y=1.25,loc ='left')
    plt.ylim(ymin=0)
    plt.xlim(xmin=0,xmax=len(x))
    plt.xticks(x,version_list,rotation=270,fontsize=12)
    #plt.xlabel('%s' % device_name,fontsize=20)
    #plt.xlabel('%s (%s/%s to %s/%s)' % (device_name,start_date,year_start,end_date,year_end),fontsize=16)
    plt.ylabel('Total Sessions Number',fontsize=16,labelpad=15)
    plt.grid()
    plt.tight_layout()
    plt.twinx()
    plt.plot(x,y2,color='green',label='HA Status')
    plt.plot(x,y3,color='red',label='FPC Status')
    plt.ylim(ymin=0)
    plt.ylabel('HA and PIC Status',fontsize=16,labelpad=15,rotation=270)
    ha_y_ticks = np.arange(0, 3, 1)
    plt.yticks(ha_y_ticks)
    plt.twiny()
    plt.xlim(xmin=0,xmax=len(x))
    plt.xticks(x,version_middle_index_list,rotation=0,fontsize=12)
    #plt.xlabel('%s' % device_name,fontsize=18)
    #plt.xlabel('Blue Line (Total Sessions Number), Green Line (HA:Pass=1,Fail=0), Red Line (PIC:Pass=2,Fail=0)',fontsize=14)
    ax1.get_yaxis().get_major_formatter().set_scientific(False)
    ax1.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.tight_layout()
    if platform.system()=='Linux':
        plt.savefig("/var/www/html/log/%s_status.png" % device_name, dpi=200, transparent=True, pad_inches = 0)
    else:
        plt.savefig("%s_status.png" % device_name, dpi=200, transparent=True, pad_inches = 0)
    plt.close(fig)

interval=31
date_list=get_date_list(interval)
print date_list
csv_list=[]
for date_item in date_list:
    csv_name=('device-facts_%s*' % date_item)
    csv_list=csv_list+glob.glob(csv_name+'.csv')
csv_list.sort()
print csv_list
timeline_list=[]
year_start=csv_list[0].split('_')[1].split('-')[0]
year_end=csv_list[-1].split('_')[1].split('-')[0]
for item in csv_list:
    item=item.split('.')[0]
    item_date=item.split('_')[1]
    item_time=item.split('_')[2]
    timeline_list.append('%s/%s %s:%s' % (item_date.split('-')[1],item_date.split('-')[2],item_time.split('-')[0],item_time.split('-')[1]))
timeline_list.sort()
#print timeline_list
if platform.system()=='Linux':
    if os.path.exists('/home/regress/Ansible/facts/log/device-facts.csv')==True:
        os.remove('/home/regress/Ansible/facts/log/device-facts.csv')
else:
    if os.path.exists('/Users/ryanliu/Downloads/Ansible/facts/log/device-facts.csv')==True:
        os.remove('/Users/ryanliu/Downloads/Ansible/facts/log/device-facts.csv')
for f in csv_list:
    df=pd.read_csv(f)
    df.to_csv('log/device-facts.csv', index=False, header=False, mode='a+')
df_init=pd.read_csv('log/device-facts.csv', header=None, names=['name','version','booted_time','type','session','HA','fpc','time'],low_memory=False)
df=df_init.copy()
df_time=df_init.copy()
df_log1=df_init.copy()
#df_time=df_init.copy()
print df


version_list_dict=write_version_csv(df,name_list)
print version_list_dict
#df=pd.read_csv('device-facts.csv', header=None, names=['name','version','booted_time','type','session','HA','fpc','time'],low_memory=False)
df=df_init
#df.drop(['time','type','HA'],axis=1,inplace=True)
df.drop(['booted_time','type','time'],axis=1,inplace=True)
#df=df.drop_duplicates()
write_session_csv(df)

df_log2=pd.read_csv('log/session-ha-fpc_info.csv',low_memory=False)
df_log3=pd.read_csv('log/session-ha-fpc_info_init.csv',low_memory=False)
df_error=df_log2.copy()
write_log_csv(df_log1,df_log2,df_log3)


df_version_info=pd.read_csv('log/version_info.csv', low_memory=False)
start_date=timeline_list[0].split()[0]
end_date=timeline_list[-1].split()[0]
timeline_list_full=timeline_list
for item in name_list:
    timeline_list=timeline_list_full
    df2=df.loc[df['name']==item]
    #print df2
    #df2=df2.reset_index(drop=True)
    #df2.drop(['name'],axis=1,inplace=True)
    #version_list_init_0=version_list_dict['%s' % item]
    #df2['version']=df2['version'].astype('category')
    #df2['version'].cat.set_categories(version_list_init_0, inplace=True)
    #print df2
    #df2.sort_values('version', inplace=True)
    #df2=df2.reset_index(drop=True)
    #print df2
    #print df2['session']
    #df3=df2.groupby(by='version')['session'].apply('|'.join).reset_index()
    #print df3
    #device_name='slt28-palm'
    version_list=[]
    version_list_short=[]
    uptime_list=[]
    x=[]
    y=[]
    y_ha=[]
    y_fpc=[]
    y_status=[]
    for item_session in df2['session'].to_list():
        y.append(int(item_session))
    for item_ha in df2['HA'].to_list():
        y_ha.append(int(item_ha))
    for item_fpc in df2['fpc'].to_list():
        y_fpc.append(int(item_fpc))
    for i in range(len(y_ha)):
        y_status.append(y_ha[i]+y_fpc[i])
    
    version_list_full=df2['version'].to_list()
    for i in range(len(version_list_full)):
        x.append(i)
        if version_list_full[i] not in version_list_short:
            version_list_short.append(version_list_full[i])
        if i==0:
            version_list.append(version_list_full[i])
        else:
            if version_list_full[i]==version_list_full[i-1]:
                version_list.append('')
            else:
                version_list.append(version_list_full[i])
    print len(version_list_full)
    print timeline_list
    print Counter(version_list_full)
    if len(version_list_full)!=len(timeline_list):
       timeline_list=timeline_list_full[-(len(version_list_full)):]
    
    xticks_dataframe=pd.DataFrame({'version':version_list_full})
    #xticks_dataframe['time']=timeline_list
    print xticks_dataframe
    
      
    #data_frame1=xticks_dataframe.reset_index().groupby('version')['index'].apply(np.array)
    xticks_dataframe['block'] = (xticks_dataframe.version.shift(1) != xticks_dataframe.version).astype(int).cumsum()
    #print xticks_dataframe
    data_frame1=xticks_dataframe.reset_index().groupby(['version','block'])['index'].apply(np.array)
    #print xticks_dataframe
    index_list=[]
    start_end_index_list=[]
    middle_index_list=[]
    #print x[-1]
    print data_frame1
    print len(data_frame1)
    add_last_index=1
    for i in range(len(data_frame1)):
        
        if data_frame1[i][-1]==x[-1]:
            index_list=index_list+data_frame1[i][:].tolist()
            start_end_index_list.append(data_frame1[i][0])
            start_end_index_list.append(data_frame1[i][-1])
            if len(data_frame1[i][:])>=6:
                add_last_index=0
                if (len(data_frame1[i][:])%2)==0:
                    middle_index_list.append(data_frame1[i][len(data_frame1[i][:])/2-1])
                else:
                    middle_index_list.append(data_frame1[i][(len(data_frame1[i][:])-1)/2-1])
        else:
            if len(data_frame1[i][:])>=6:
                index_list=index_list+data_frame1[i][:].tolist()
                start_end_index_list.append(data_frame1[i][0])
                start_end_index_list.append(data_frame1[i][-1])
                if (len(data_frame1[i][:])%2)==0:
                    middle_index_list.append(data_frame1[i][len(data_frame1[i][:])/2-1])
                else:
                    middle_index_list.append(data_frame1[i][(len(data_frame1[i][:])-1)/2-1])
    i_counter=0
    x_short_list=[]
    y_short_list=[]
    y_ha_short_list=[]
    y_fpc_short_list=[]
    version_short_list=[]
    version_short_list_null=[]
    version_list_bar=[]
    timeline_short_list=[]
    timeline_start_end_index_list=[]
    version_middle_index_list=[]
    print len(x)
    print len(timeline_list)
    print len(timeline_list_full)
    print len(version_list_full)
    
    for i in range(len(x)):
        if i in index_list:
            y_short_list.append(y[i])
            y_ha_short_list.append(y_ha[i])
            y_fpc_short_list.append(y_fpc[i])
            x_short_list.append(i_counter)
            i_counter+=1
            version_short_list.append(version_list_full[i])
            timeline_short_list.append(timeline_list[i])
            if i in start_end_index_list:
                timeline_start_end_index_list.append(timeline_list[i])
            else:
                timeline_start_end_index_list.append('')
            if i in middle_index_list:
                version_middle_index_list.append(version_list_full[i])
            else:
                version_middle_index_list.append('')
    if add_last_index!=0:
        version_middle_index_list[-1]=version_list_full[-1]
    for i in range(len(version_short_list)):
        if version_short_list[i] not in version_list_bar:
            version_list_bar.append(version_short_list[i])
        if i==0:
            version_short_list_null.append(version_short_list[i])
        else:
            if version_short_list[i]==version_short_list[i-1]:
                version_short_list_null.append('')
            else:
                version_short_list_null.append(version_short_list[i])
    print timeline_short_list
    print version_short_list
    print version_middle_index_list
    #print index_list
    #print data_frame1
    #x=[]
    #y=[]
    #print len(df2['version'])
    #for i in range(len(df2['version'])):
        #print df2['version'][i]
    #    x.append(i)
    #    y.append(int(df2['session'][i]))
    #    if df2['version'][i] in version_list:
    #        version_list.append('')
    #    else:
    #        version_list.append(df2['version'][i])
    #        version_list_short.append(df2['version'][i])
    
    
    for version_item in version_list_bar:
        uptime_list.append(df_version_info[(df_version_info['Unnamed: 0']=='%s' % item)]['%s' % version_item].values[0])
    print version_list_bar
    print uptime_list
    version_labels=[]
    time_values=[]
    #print version_list
    for i in range(len(version_short_list_null)):
        if version_short_list_null[i]!='':
            version_short_list_null[i]='%s\n(%s)' % (timeline_short_list[i],version_short_list[i])
            version_labels.append(version_short_list_null[i])
            time_values.append(timeline_short_list[i])
            #version_list[i]='%s' % (timeline_list[i])
            
            #version_list[i]='%s' % timeline_list[i]
    #print timeline_list
    #print version_labels
    #print time_values
    version_labels.reverse()
    time_values.reverse()
    len_version_labels=len(version_labels)
    if len(version_labels)<18:
        version_labels.extend(['']*(18-len(version_labels)))
        time_values.extend(['']*(18-len(time_values)))
    if version_list[-1]=='':
        version_list[-1]=timeline_list[-1]
    if len_version_labels<=6:
        version_labels=version_labels[:6]
        time_values=time_values[:6]
    elif len_version_labels<=12:
        version_labels=version_labels[:12]
        time_values=time_values[:12]
    else:
        version_labels=version_labels[:18]
        time_values=time_values[:18]
    
    #print version_labels
    #print time_values
    print len(x_short_list)
    print len(timeline_start_end_index_list)
    print len(version_middle_index_list)
    print version_short_list_null
    for i in range(len(timeline_start_end_index_list)):
        if i!=0 and i!=len(timeline_start_end_index_list)-1:
            if i!=len(timeline_start_end_index_list)-2:
                if timeline_start_end_index_list[i]!='' and timeline_start_end_index_list[i+1]!='':
                    timeline_start_end_index_list[i-1]=timeline_start_end_index_list[i]
                    timeline_start_end_index_list[i]='-----------------'
            else:
                if timeline_start_end_index_list[i]!='' and timeline_start_end_index_list[i+1]!='':
                    timeline_start_end_index_list[i+1]=''
    
    #print timeline_start_end_index_list
    #print version_middle_index_list
    #for i in range(len(timeline_start_end_index_list)):
    #    if version_middle_index_list[i]!='':
    #        if version_middle_index_list[i]!=version_list_full[-1]:
    #            timeline_start_end_index_list[i]='[%s]' % version_middle_index_list[i]
    #    if i!=len(version_middle_index_list)-1:
    #        version_middle_index_list[i]=''
    #    else:
    #        version_middle_index_list[i]=version_list_full[-1]
    iter_list=[]
    #if version_middle_index_list[-1]=='':
    for i in range(len(timeline_start_end_index_list)):
        if version_middle_index_list[i]!='':
            timeline_start_end_index_list[i]=version_middle_index_list[i]
            version_middle_index_list[i]=''
    print timeline_start_end_index_list
    for k,v in itertools.groupby(timeline_start_end_index_list):
        iter_list.append(list(v))
    print iter_list
    print timeline_start_end_index_list
    print version_middle_index_list
    for i in range(len(timeline_start_end_index_list)):
        if timeline_start_end_index_list[i] in version_list_full:
                for counter in range(len(iter_list)):
                    if iter_list[counter][0]==timeline_start_end_index_list[i] and counter!=len(iter_list)-1:
                        if counter!=len(iter_list)-3:
                            if (len(iter_list[counter-1])+len(iter_list[counter+1]))>1.2*len(iter_list[counter][0]):
                                version_middle_index_list[i]=timeline_start_end_index_list[i]
                                timeline_start_end_index_list[i]=''
                                iter_list=iter_list[counter+3:]
                            break 
                        else:
                            if (len(iter_list[counter-1])+len(iter_list[counter+1]))>1.1*len(iter_list[counter][0]):
                                version_middle_index_list[i]=timeline_start_end_index_list[i]
                                timeline_start_end_index_list[i]=''
                            break
    #else:
    if timeline_start_end_index_list[-1]!='' and timeline_start_end_index_list[-2]!='':
        if timeline_start_end_index_list[-2]!='-----------------':
            #timeline_start_end_index_list[-1]=version_list_full[-1]
            timeline_start_end_index_list[-2]=''
        #else:
        #    timeline_start_end_index_list[-1]=version_list_full[-1]
    #else:
    #    timeline_start_end_index_list[-1]=version_list_full[-1]
    #print timeline_start_end_index_list
    print version_middle_index_list
    version_list_bar.reverse()
    uptime_list.reverse()
    if item=='nonibert':
        bar_line_chart(x_short_list,y_short_list,y_ha_short_list,y_fpc_short_list,timeline_start_end_index_list,item,version_labels,time_values,version_list_bar,uptime_list,start_date,year_start,end_date,year_end,version_middle_index_list)
        bar_chart(version_list_bar,uptime_list,item,start_date,year_start,end_date,year_end)
    for i in range(len(timeline_start_end_index_list)):
        if '_' in timeline_start_end_index_list[i]:
            timeline_start_end_index_list[i]=timeline_start_end_index_list[i].split('_')[0]
    print timeline_start_end_index_list
    if item=='nonibert':
        status_line_chart(x_short_list,y_short_list,y_ha_short_list,y_fpc_short_list,timeline_start_end_index_list,item,start_date,year_start,end_date,year_end,version_middle_index_list)
#print name_list
error_testbed_list=get_error_testbed_list(df_error,name_list)
device_name_dict={"TCS":name_list_tcs,"CNRD":name_list_regression,"MiniPDT":name_list_minipdt,"All":name_list,"Error":error_testbed_list}
write_html(start_date,year_start,end_date,year_end,device_name_dict,name_list,cnrd_owner_dict,tcs_owner_dict)
