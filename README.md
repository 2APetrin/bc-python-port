# BC Python Port
BC Python Port - это Python-интерфейс для криптографической библиотеки [Bouncy Castle](https://www.bouncycastle.org/).
> The Bouncy Castle project offers open-source APIs for Java, C# and Kotlin that support cryptography and cryptographic protocols.

Проект позволяет разрабатывать приложения, использующие все возможности Bouncy Castle, на языке Python.
## Запуск
Для сборки и последующего запуска необходимо
### Установить Python и pip, используются ``Python 3.12.3`` и ``pip 24.0``
Для debian-based дистрибутивов Linux
```
sudo apt install python3
```
Для Windows использовать установщик с [официального сайта](https://www.python.org/downloads/release/pymanager-250/) или установить из Microsoft Store. При использовании установщика выбрать **.msix** файл, а не .msi. \
Если не удаётся выполнить установку .msix обычным способом, то воспользоваться PowerShell:
```
Add-AppxPackage .\Downloads\python-manager-25.0.msix
python
```
### Установить зависимости для Python
Рекомендуется создать Python virtual environment и установить пакеты туда, чтобы всё хранилось в папке с проектом. Для этого из корневой папки проекта выполнить
```
python3 -m venv .venv
```
Активировать среду (в Linux)
```
source ./.venv/bin/activate
```
Активировать среду (в Windows, использовать PowerShell)
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```
Установить зависимости
```
pip install -r requirements.txt
```
### Установить Java (JDK), используется `openjdk 21.0.8 2025-07-15`
Для debian-based дистрибутивов Linux
```
sudo apt install openjdk-21-jdk
```
Для Windows использовать установщик c [официального сайта](https://www.oracle.com/java/technologies/downloads/?er=221886#jdk25-windows).
После этого из PowerShell добавить Java в PATH
```
$Env:PATH += ";C:\Program Files\Java\jdk-25\bin"
```

### Установить [Maven](https://maven.apache.org/install.html), используется `Apache Maven 3.8.7`

Для debian-based дистрибутивов Linux
```
sudo apt install maven
```
Для Windows скачать [Binary Distribution](https://maven.apache.org/download.cgi). Распаковать в корневую директорию проекта и оттуда добавить в PATH
```
$Env:PATH += ";.\apache-maven-3.9.11\bin"
```
### Собрать Java-часть с помощью maven
```
mvn package
```
### Запустить требуемый python-файл, например, ``example00.py``
```
python3 example00.py
```

## Генерация SBOM
- Для генерации SBOM требуется скачать `cyclonedx-cli` из официального [репозитория](https://github.com/CycloneDX/cyclonedx-cli/releases/tag/v0.29.1). Затем поместисть скачанный файл в корневую папку проекта.
- Активировать среду Python (см. п. Запуск)
- Для генерации SBOM в Linux *из корневой папки проекта* запустить ``generate_sbom.sh``.
```
chmod u+x generate_sbom.sh && ./generate_sbom.sh
```
- Для Windows *из корневой папки проекта* запустить в PowerShell ``generate_sbom.ps1``.
```
.\generate_sbom.ps1
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
