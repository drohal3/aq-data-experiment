requires docker

```bash
docker-compose up
```

Running with 3 devices sending 1 message per second, 5 messages in total each:
```
rohal@Dominiks-MacBook-Air connect_device_package % docker-compose up
[+] Running 1/0
 ⠿ Container measurements  Created                                                                                                                                     0.0s
Attaching to measurements
measurements  | Connecting to <???>.eu-central-1.amazonaws.com with client ID 'cpc-testClient'...
measurements  | Connected!
measurements  | creating devices...
measurements  | created 3 devices!
measurements  | simulating...
measurements  | topic: cpc/main, data: {'device_id': '0'}
measurements  | topic: cpc/main, data: {'device_id': '1'}
measurements  | topic: cpc/main, data: {'device_id': '2'}
measurements  | topic: cpc/main, data: {'device_id': '0'}
measurements  | topic: cpc/main, data: {'device_id': '1'}
measurements  | topic: cpc/main, data: {'device_id': '2'}
measurements  | topic: cpc/main, data: {'device_id': '0'}
measurements  | topic: cpc/main, data: {'device_id': '1'}
measurements  | topic: cpc/main, data: {'device_id': '2'}
measurements  | topic: cpc/main, data: {'device_id': '0'}
measurements  | topic: cpc/main, data: {'device_id': '1'}
measurements  | topic: cpc/main, data: {'device_id': '2'}
measurements  | topic: cpc/main, data: {'device_id': '0'}
measurements  | topic: cpc/main, data: {'device_id': '1'}
measurements  | topic: cpc/main, data: {'device_id': '2'}
measurements  | Simulation of device 0 finished after 5.026923894882202 seconds!
measurements  | Simulation of device 1 finished after 5.024030447006226 seconds!
measurements  | Simulation of device 2 finished after 5.0239222049713135 seconds!
measurements  | elapsed time: 5.028521537780762
measurements exited with code 0
```