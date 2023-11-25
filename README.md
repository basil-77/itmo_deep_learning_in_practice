# Распознавание дорожных знаков с помощью компьютерного зрения
## Разработка мобильного приложения

Данный проект выполнен в рамках курса "Глубокое обучение на практике" от магистратуры ITMO AI Talent Hub.

## Описание используемых данных

Для обучения модели был выбран датасет [RTSD](https://www.kaggle.com/datasets/watchman/rtsd-dataset). Изображения получены с широкоформатного видеорегистратора, который снимает с частотой 5 кадров в секунду. Разрешения изображений от 1280×720 до 1920×1080. Фотографии были сделаны в разное время года (весна, осень, зима), в разное время суток (утро, день, вечер) и при различных погодных условиях (дождь, снег, яркое солнце). В наборе используется 155 знак дорожного движения, формат разметки - COCO.


## Подготовка данных для обучения
Данные, использованные для обучения представлены с разметкой COCO. Модели YOLO требуют собственый формат представления, соответственно было выполнено преобразование данных в YOLO-формат. Для преобразования использовался скрипт JSON2YOLO, представленный на [Ultralytics](https://github.com/ultralytics/JSON2YOLO). Процесс конвертации - в файле prepare_data.ypinb.

## Выбор модели и обучение

Поскольку обученную модель предполагается использовать в мобильном приложении одним из основных критериев выбора (помимо актуальности и точности) являлась "легкость" - таким образом выбор был сделан в пользу версии 'nano' (YOLOv8n) - самой быстрой и маленькой из серии YOLO8.

```python
model = YOLO('yolov8n.pt')
model.info()

results = model.train(data='./trafic_signs.yaml', batch=-1, epochs=20, imgsz=640, device='0')
```
Обучение модели производилось со следующими параметрами: 
Batch-size - автовыбор;  
Размер входного изображений - 640 (руководствуясь теми же соображениями относительно легкости и скорости работы);  
Оптимизатор - автовыбор;  
Число эпох - 20.  
Использовалась GPU Nvidia RTX 3060 12Gb.  
Графики изменения метрик в процессе обучения:  

По окончании обучения оценка метрик mAP50 и mAP50-95 составили соответственно.

## Разработка MVP (мобильное приложение Android)
Использование модели в мобильном приложении требует предварительной ее конвертации в совместимый формат. В данной работе выполнена конвертация в torchscript ptl:

```python
model.export(format='torchscript')
```
```python
torchscript_model = "yolov8n.torchscript"
export_model_name = "yolov8n.torchscript.ptl"

model = torch.jit.load(torchscript_model)
optimized_model = optimize_for_mobile(model)
optimized_model._save_for_lite_interpreter(export_model_name)

print(f"mobile optimized model exported to {export_model_name}")
```

В качестве образца приложения использован шаблон PyTorch Android App, доступный на гитхаб [PyTorch Android App](https://github.com/pytorch/android-demo-app/tree/master). Шаблон разработан под версию YOLOv5. Выбранная в качестве модели восьмая версия имеет отличия в output shape - для версии 5 output shape имеет формат [1, 22500, nClasses+5], в то время как, в версии 8 формат выхода представляет собой тензор размерности [1, nClasses+4, 8400]. Данные различия в форматах потребовали изменений реализации постобработки Non Maximum Supression, что и было сделано в рамках работы ([outpotsToNMSPredictionsYOLO8()](https://github.com/basil-77/itmo_deep_learning_in_practice/blob/b4e4f94cb6a94bbd9fb46e1683484062ad2accf3/app/app/src/main/java/org/pytorch/demo/objectdetection/PrePostProcessor.java#L153) в модуле PrePostProcessor.java).

```java
static ArrayList<Result> outputsToNMSPredictionsYOLO8(float[] outputs, float imgScaleX, float imgScaleY, float ivScaleX, float ivScaleY, float startX, float startY)
```
Помимо этого был переработан основной экран (Activity) приложения и добавлена дополнительная функциональность исходя из задачи. Пороговое значение вероятности для фиксации факта детекции - 0.5  
Работа выполнена в среде Android Studio.  
Сборка приложения выполнялась под платформу API 31 (Android 12).  

## Как запустить

