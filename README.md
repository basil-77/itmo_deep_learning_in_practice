# Распознавание дорожных знаков с помощью компьютерного зрения

Данный проект выполнен в рамках курса "Глубокое обучение на практике" от магистратуры ITMO AI Talent Hub.

## Описание используемых данных

Для обучения модели был выбран датасет [RTSD](https://www.kaggle.com/datasets/watchman/rtsd-dataset). Изображения получены с широкоформатного видеорегистратора, который снимает с частотой 5 кадров в секунду. Разрешения изображений от 1280×720 до 1920×1080. Фотографии были сделаны в разное время года (весна, осень, зима), в разное время суток (утро, день, вечер) и при различных погодных условиях (дождь, снег, яркое солнце). В наборе используется 155 знак дорожного движения, формат разметки - COCO.

Подробный анализ датасета (EDA) находится в файле: "EDA_Russian_traffic_signs.ipynb"

<p align="center"><img src="img/EDA_1.jpg" width=80% alt="Main page"></p>

Также можно увидеть что из себя представляют изображения данного датасета:

<p align="center"><img src="img/1.jpg" width=80% alt="Main page"></p>
<p align="center"><img src="img/2.jpg" width=80% alt="Main page"></p>

## Подготовка данных для обучения
Данные, использованные для обучения представлены с разметкой COCO. Модели YOLO требуют собственый формат представления, соответственно было выполнено преобразование данных в YOLO-формат. Для преобразования использовался скрипт JSON2YOLO, представленный на [Ultralytics](https://github.com/ultralytics/JSON2YOLO). Процесс конвертации - в файле prepare_data.ypinb.

## Эксперименты

Были взяты четыре модели, все они представлены в таблице ниже. Модели были запущены в одних условиях и обучены на 20 эпохах.
| Metrics  | YOLOv5su | YOLOv8n  | YOLOv8n640 | YOLOv8s640 |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| `precision` | 0.74297  | 0.81094  | 0.72414  | 0.79494  |
| `recall`  | 0.74024  | 0.7301  | 0.63267  | 0.75753  |
| `mAP50`  | 0.80417  | 0.81824  | 0.70368  | 0.83163  |
| `mAP50-95`  | 0.60305  | 0.62838  | 0.51832  | 0.62737  |

<p align="center"><img src="img/recall.png" width=80% alt="Main page"></p>

### Inference 
- YOLO8 1280 cpu: 3ms preprocess 72ms inference 1.5 postprocess cuda: 3.5 ms preprocess 4ms inference 0.5 postprocess
- YOLO8s 640 cpu: 1ms 50ms 1ms cuda 0.5ms 4.5ms 1ms
cpu - core i513600 cuda: rtx 4070ti

=======

## MVP

Итоговый продукт представляет собой веб-сервис + Android приложение.

Веб-приложение позволяет загрузить видеоряд с локального ПК или с YouTube. Если на видео будет обнаружен знак дорожного движения, то в реальном времени он будет выделен bounding-box'ом с текстовой подписью номера знака из ПДД. Например:

<p align="center"><img src="img/result_det.jpg" width=90% alt="Main page"></p>

Внешний вид интерфейса веб-сервиса

<p align="center"><img src="img/web.png" width=90% alt="Main page"></p>

- Веб-приложение: streamlit
- Модель: YOLOv8m

### Запись функционала для веб-сервиса

- [Светло день](https://youtu.be/1IzePzng8G8)

- [Дождь ночь](https://youtu.be/OCR3bonUP80)

### Android-приложение

Приложение позволяет в реальном времени получать информацию о знаках дорожного движения в кадре смартфона. 
<p align="center"><img src="img/1rds.jpg" height = 350 width=210 alt="Main page"><img src="img/2rds.jpg" height = 350 width=210 alt="Main page"></p>

Демонстрация работы приложения в реальных условиях:

[![Watch the video](https://i.stack.imgur.com/Vp2cE.png)](https://www.youtube.com/watch?v=2pB8IUU6EoA)

## Как запустить веб-сервис

### Requirements python >= 3.10
```bash
pip install -r requirements.txt
```

### Запуск из папки проекта
```bash
streamlit run app.py
```
После 1-го запуска установится доп библиотека. Нужно будет перезапустить сервис еще раз.

## Как установить и использовать Android-приложение

Приложение опубликовано в RuStore и доступно для загрузки по [ссылке](https://apps.rustore.ru/app/org.pytorch.demo.objectdetection) или QR-код
<p align="center">
 <img width="200px" src="img/qr.jpg" alt="qr"/>
</p>
