# TEST-PB
Тестовое задание <br>
В проекте создаются <br>
  - контейнеры с БД Oracle (2 отдельных контейнера с двумя экземплярами) 
  - контейнер с liquibase
  - контейнер с программой python

Все контейнеры запускаются в docker-compose. <br>
Исходные данные:<br>
 <p>В каталоге \liquibase\changelog\ хранятся XML и CSV файлы, в которых описаны структуры хранения и данные.</p>
 <p>В каталоге \python-client\ хранится файл s3access.csv, в котором нужно прописать User Name,Access key ID,Secret access key для доступа к AmazonS3.</p>
 
Предусловия: <br>
  - установить docker
  - установить docker-compose
  - создать bucket в AmazonS3 с именем pb.report
  - заполнить файл s3access.csv своими учетными данными
  - пересоздать image python-client:
    `PS C:\docker\TEST-PB\python-client> docker build . -t python-client` <br> 

Для сборки перейти в каталог TEST-PB (в нем должен быть docker-compose.yml) и выполнить в командной строке команду (в Windows PowerShell ее вид следующий):<br>
`PS C:\docker\TEST-PB> docker-compose up`<br>

Если необходимо загрузить "свои" данные, можно внести изменения в файлы каталога \liquibase после чего перестроить image <br>
`PS C:\docker\TEST-PB\liquibase> docker build . -t my-liquibase` <br>
и снова пересоздать контейнер: <br>
`PS C:\docker\TEST-PB> docker-compose up` <br>
В результате работы программы python в bucket AmazonS3 с именем pb.report должен быть создан файл report-pandas-simple.csv который хранит результат вычислений согласно условию ТЗ.

Известные ограничения:<br>
Т.к. в программе на python прописаны имя bucket и условие расчета (SQL) то можно изменять только наполнение данных, но не их структуры.<br>
Все структуры хранятся в Oracle схеме VITALII.<br>
Для синхронизации работы контейнеров используются скрипты (wait.sh и wait-python.sh).<br>
Также, сама программа на python выполняет проверку наличия данных в таблице PURCHASES и выполняет ряд попыток подключения к БД с задержкой между попытками.

    
