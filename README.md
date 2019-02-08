# Weblogic Client

## Funzionalità

- service

    permette di gestire il ciclo di vita dei server (istanze applicative)

    ```bash
    $ ./wlst.sh service.py status --server=web01
    SHUTDOWN
    $

    $ ./wlst.sh service.py start --server=web01
    $ echo $?

    $ ./wlst.sh service.py stop --server=web01
    $ echo $?
    ```

- cluster

    permette di gestire le risorse cluster

    ```bash
    $ ./wlst.sh cluster.py status --cluster=web-CLU
    Computer            Status
    web02               SHUTDOWN
    web01               RUNNING
    ```


- deployer 
:wq

    utilizzato per effettuare il deploy delle applicazioni

    se il deploy deve essere effettuato a livello cluster, è necessario invocare lo script con l'opzione --cluster




