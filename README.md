# Ключи командной строки

Ключи для указания адресов и/или сетей и подсетей для сканирования
    
    --address '[ipv4 address], [ipv4 address range] ... '
                
        [ipv4 address] - сетевой адрес: 
        192.168.0.1
        
        [ipv4 address range] - диапазон сетевых адресов
        диапазон сетевых адресов задается в следующем виде:
        192.168.0.1 - 192.168.0.100
        
        Пример использования:
        --address '192.168.0.1, 192.168.0.100 - 192.168.0.200, 192.168.0.10' 
        
    --network '[ipv4 network]'
        
        [ipv4 network] - сеть ipv4 задается с маской:
        
        10.4.0.0/16 или 172.20.16.0/20
        
        Пример использования:
        --network '10.4.0.0/16, 10.1.0.0/16, 10.0.0.0/26'

    Допускается использование одновременно и --address и --network
    
Параметры управления скоростью сканирования

    -s --step [integer]
    
        integer - целое число от 1 до 800
        
        Шагом регулируется скорость сканирования диапазона
       
    -t --timeout [seconds]
    
        seconds - целое число в секкундах от 1 до ...
        
    Все вместе работает следующим образом:
        
        Общий диапазон адресов, например 10.4.0.0/16 ~ 64516 адресов
        
        В единицу времени, которая задается параметром timeout, выбирается часть адресов, 
        количество которых регулируется шагом [step] - отправляются на сканирование.
        
        Например, при шаге в 200 адресов и таймаутре 2 секунды механизм работы следующий: 
            
        из пула адресов сети  10.4.0.0/16 выбираются первые 200 адресов:
        10.4.0.0 - 10.4.0.199 и пингуются, следующий диапазон выбирается через указанный timeout
        
Управление выводом

    -v --verbose [True/False] - булевый параметр
       
        выводит на стандартный вывод информацию:
        - Расчет времени на сканирование
        - Список ответивших хостов
        - Список ошибок в принятых пакетах
    
    -e --errors [True/False] - булевый параметр
    
        выводит на стандартный вывод список ошибок в принятых пакетах
        
    -S --silence [True/False] - булевый параметр
    
        "молчаливый" режим
        
        На стандартный вывод не выводит ничего
    
    Без ключей будет выведена информация:
        - Список ответивших хостов
        - Затраченое время
        - Количество просканированных адресов
        - Количество ответивших хостов
        - Количество ответов с ошибками
         
# Предварительный расчет производительности
    Открытые сокеты icmp
    ss -l | grep 'icmp' | grep -v 'ipv6' | wc -l
    
    Открытые сокеты НЕ icmp
    ss -l | grep -Ev 'icmp|ipv6' | wc -l
    
    # requester.timeout = 1
    # 225 / 1 = 225 - OK
    # 250 / 1 = 250 - OK
    # 300 / 1 = 300 - OK    max: 300
    # 325 / 1 = 325 - NOT
    # 350 / 1 = 350 - NOT
    # 400 / 1 = 400 - NOT
    # 450 / 2 = 225 - OK    max: 450
    # 500 / 2 = 250 - NOT   max: 500
    # 600 / 2 = 300 - NOT   max: 600
    # 450 / 3 = 150 - OK    max: 450
    # 500 / 3 = 166 - NO    max: 500
    # 600 / 3 = 200 - NOT   max: 600
    # 700 / 3 = 233 - NOT   max: 700
    # 850 / 3 = 212 - NOT   max: 850
    # 300 / 4 = 75  - OK    max: 300
    # 400 / 4 = 100 - OK    max: 400
    # 500 / 4 = 125 - OK    max: 500
    # 850 / 4 = 212 - OK    max: 850
    # 800 / 5 = 160 - OK    max: 800
    # 850 / 5 = 170 - OK    max: 850
    #-------------------------------------
    # 1000 / 5 = 200 - OK   max: 1000
    # 1500 / 5 = 300 - NOT  max: 1500