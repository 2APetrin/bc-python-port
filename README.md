# BC Python Port
BC Python Port - это Python-интерфейс для криптографической библиотеки [Bouncy Castle](https://www.bouncycastle.org/).
> The Bouncy Castle project offers open-source APIs for Java, C# and Kotlin that support cryptography and cryptographic protocols.

Проект позволяет разрабатывать приложения, использующие все возможности Bouncy Castle, на языке Python.
## Запуск
Для сборки и последующего запуска необходимо
- Установить Python и pip, используются ``Python 3.12.3`` и ``pip 24.0``

Для debian-based дистрибутивов Linux
```
sudo apt install python3
```
Для Windows использовать установщик с [официального сайта](https://www.python.org/downloads/release/pymanager-250/).
- Установить зависимости для Python
```
python3 -m pip install -r requirements.txt
```
Вместо этого **опциально** можно создать Python virtual environment и установить пакеты туда, чтобы всё хранилось в папке с проектом:
```
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```
- Установить Java (JDK), используется `openjdk 21.0.8 2025-07-15`

Для debian-based дистрибутивов Linux
```
sudo apt install openjdk-21-jdk
```
- Установить [Maven](https://maven.apache.org/install.html), используется `Apache Maven 3.8.7`

Для debian-based дистрибутивов Linux
```
sudo apt install maven
```
- Собрать Java-часть с помощью maven
```
mvn package
```
- Запустить требуемый python-файл, например, ``lazy_behaviour.py``
```
python3 lazy_behaviour.py
```

## Генерация SBOM
Для генерации SBOM следует *из корневой папки проекта* запустить ``generate_sbom.sh``
```
chmod u+x generate_sbom.sh && ./generate_sbom.sh
```
Это создаст java-SBOM в папке ``./target`` и python-SBOM в корневой папке проекта, после чего объединит их в один файл ``sbom.json``

## Используемые инструменты
- **Maven** - система сборки Java-проектов, позволяющая удобно создавать .jar файлы, включающие в себя все зависимости, необходимые для работы программы (fat jar).  
- **py4j** - python-библиотека, позволяющая получать доступ к объектам Java из Python.
- **CycloneDX** (cyclonedx-python и cyclonedx-cli) - набор [инструментов](https://cyclonedx.org/capabilities/sbom/) для создания SBOM (Software Bill Of Materials) в формате OWASP CycloneDX.

## Схема работы
Для соединения Python и Java используется библиотека Py4j. Py4J позволяет программам на Python, запущенным в интерпретаторе Python, динамически обращаться к объектам Java на виртуальной машине Java. Методы вызываются так, как если бы объекты Java находились в интерпретаторе Python, а к коллекциям Java можно было бы получить доступ с помощью стандартных методов сбора данных Python. Py4J также позволяет Java-программам вызывать объекты Python.

Py4J — это мост между Python и Java, построенный на сетевом протоколе поверх TCP-сокета.
Python и JVM обмениваются сообщениями по сети (localhost:port). Не используются JNI (Java Native Interface), Jython, C-биндингов или shared memory — только TCP-соединение и сериализация данных.

```
+--------------------+             TCP socket              +---------------------+
|     Python side    |  <--------------------------------> |     Java side       |
|  py4j.java_gateway |     (by default 127.0.0.1:25333)    |  py4j.GatewayServer |
+--------------------+                                     +---------------------+
```

В модуле lazy_behaviour.py фукнция ``def get_gateway(timeout_seconds=30)`` создает подключение к Java если оно еще не создано, или возвращает объект подключения, если создано. Для защиты используется случайно генерирующийся при каждом создании соединения токен.

## Структура проекта
- `./scr/` - Java-файлы для создания сервера 
- `./generate_sbom.sh` - скрипт для герерации SBOM в формате JSON, продуктами работы являются `sbom-python.json`, `sbom.json`.
- `./pom.xml` - конфигурационный файл Maven
- `./requirements.txt` - зависимости для Python
