import cv2
import numpy as np
import uuid
import os
import time
import wget
import easyocr
import tensorflow as tf
import sys
import object_detection
from object_detection.utils import config_util
from object_detection.protos import pipeline_pb2
from google.protobuf import text_format
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
#from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def LPDetector(Filename):
    """Parses an image (.jpg, .jpeg or .png) of a Jamaican License Plate and returns the registration number as a string."""
    
    CustomizedModelName = 'my_ssd_mobnet' 
    PretrainedModelName = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8'
    PretrainedModelURL = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz'
    TFRecordScriptName = 'generate_tfrecord.py'
    LabelMapName = 'label_map.pbtxt'

    paths = {
        'UPLOADSPATH': os.path.join('uploads'),
        'FLAGGEDPATH': os.path.join('uploads','flagged'), 
        'ISSUEDPATH': os.path.join('uploads','issued'), 
        'WORKSPACE_PATH': os.path.join('app','DetectionCode','Tensorflow', 'Workspace'),
        'SCRIPTS_PATH': os.path.join('app','DetectionCode','Tensorflow','Scripts'),
        'APIMODEL_PATH': os.path.join('app','DetectionCode','Tensorflow','Models'),
        'ANNOTATION_PATH': os.path.join('app','DetectionCode','Tensorflow', 'Workspace','Annotations'),
        'IMAGE_PATH': os.path.join('app','DetectionCode','Tensorflow', 'Workspace','Images'),
        'MODEL_PATH': os.path.join('app','DetectionCode','Tensorflow', 'Workspace','Models'),
        'PRETRAINED_MODEL_PATH': os.path.join('app','DetectionCode','Tensorflow', 'Workspace','Pre-trained-models'),
        'CHECKPOINT_PATH': os.path.join('app','DetectionCode','Tensorflow', 'Workspace','Models',CustomizedModelName), 
        'OUTPUT_PATH': os.path.join('app','DetectionCode','Tensorflow', 'Workspace','Models',CustomizedModelName, 'Export'), 
        'TFJS_PATH':os.path.join('app','DetectionCode','Tensorflow', 'Workspace','Models',CustomizedModelName, 'Tfjsexport'), 
        'TFLITE_PATH':os.path.join('app','DetectionCode','Tensorflow', 'Workspace','Models',CustomizedModelName, 'Tfliteexport'), 
        'PROTOC_PATH':os.path.join('app','DetectionCode','Tensorflow','Protoc')
     }
    files = {
        'PIPELINE_CONFIG':os.path.join('app','DetectionCode','Tensorflow', 'Workspace','Models', CustomizedModelName, 'pipeline.config'),
        'TF_RECORD_SCRIPT': os.path.join(paths['SCRIPTS_PATH'], TFRecordScriptName), 
        'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], LabelMapName)
    }

    for path in paths.values():
        if not os.path.exists(path):
            if os.name == 'nt':
                os.makedirs(path)

    labels = [{'name':'licence', 'id':1}]

    with open(files['LABELMAP'], 'w') as f:
        for label in labels:
            f.write('item { \n')
            f.write('\tname:\'{}\'\n'.format(label['name']))
            f.write('\tid:{}\n'.format(label['id']))
            f.write('}\n')

    '''
    #Configure the pipeline used to trained the model.

    config = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
    config
    pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()
    with tf.io.gfile.GFile(files['PIPELINE_CONFIG'], "r") as f:                                                                                                                                                                                                                     
        proto_str = f.read()                                                                                                                                                                                                                                          
        text_format.Merge(proto_str, pipeline_config)
    pipeline_config.model.ssd.num_classes = len(labels)
    pipeline_config.train_config.batch_size = 4
    pipeline_config.train_config.fine_tune_checkpoint = os.path.join(paths['PRETRAINED_MODEL_PATH'], PretrainedModelName, 'checkpoint', 'ckpt-0')
    pipeline_config.train_config.fine_tune_checkpoint_type = "detection"
    pipeline_config.train_input_reader.label_map_path= files['LABELMAP']
    pipeline_config.train_input_reader.tf_record_input_reader.input_path[:] = [os.path.join(paths['ANNOTATION_PATH'], 'Train.record')]
    pipeline_config.eval_input_reader[0].label_map_path = files['LABELMAP']
    pipeline_config.eval_input_reader[0].tf_record_input_reader.input_path[:] = [os.path.join(paths['ANNOTATION_PATH'], 'Test.record')]

    config_text = text_format.MessageToString(pipeline_config)                                                                                                                                                                                                        
    with tf.io.gfile.GFile(files['PIPELINE_CONFIG'], "wb") as f:                                                                                                                                                                                                                     
        f.write(config_text)
    
    '''
    #####
    '''
    #Training Command Entered in terminal
    python Tensorflow\Models\models\research\object_detection\model_main_tf2.py --model_dir=Tensorflow\Workspace\Models\my_ssd_mobnet --pipeline_config_path=Tensorflow\Workspace\Models\my_ssd_mobnet\pipeline.config --num_train_steps=10000
    '''
    #####


    #Load pipeline config and build a detection model

    configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
    detection_model = model_builder.build(model_config=configs['model'], is_training=False)

    # Restore checkpoint
    #So the latest instance of the trained model is restored in this case ckpt-21
    ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
    ckpt.restore(os.path.join(paths['CHECKPOINT_PATH'], 'ckpt-21')).expect_partial()


    def detect_fn(image):
        image, shapes = detection_model.preprocess(image)
        prediction_dict = detection_model.predict(image, shapes)
        detections = detection_model.postprocess(prediction_dict, shapes)
        return detections



    category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])
    #IMAGE_PATH is the location at which the image being analyzed for the licence plate is stored

    Picture_Test = str(Filename) 
    IMAGE_PATH = os.path.join(paths['UPLOADSPATH'],Picture_Test)


    img = cv2.imread(IMAGE_PATH)
    image_np = np.array(img)

    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)
    #detections from the tensor flow model are stored in detections

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    label_id_offset = 1
    image_np_with_detections = image_np.copy()

    viz_utils.visualize_boxes_and_labels_on_image_array(
                image_np_with_detections,
                detections['detection_boxes'],
                detections['detection_classes']+label_id_offset,
                detections['detection_scores'],
                category_index,
                use_normalized_coordinates=True,
                max_boxes_to_draw=5,
                min_score_thresh=.7,
                agnostic_mode=False)

    #min_score_thresh represents the percent of certainty(confidence metric) the model has that it correctly detected the licence plate
    #plt.imshow(cv2.cvtColor(image_np_with_detections, cv2.COLOR_BGR2RGB))
    #plt.savefig("myidentifiedplate.jpg")
    #image_np_with_detections represents our image with its detection
    #plt.show()

    #SECTION WHERE WE APPLY OCR

    detection_threshold = 0.7

    image_withdetect = image_np_with_detections

    region_threshold = 0.25


    def filter_text(region, ocr_result, region_threshold):
        #Gives use the size of our rectangle
        rectangle_size = region.shape[0]*region.shape[1]
        #stores our results
        plate = [] 
        for result in ocr_result:
            #Subtracting coordinates to get our length and them np.sum to get a single value
            length = np.sum(np.subtract(result[0][1], result[0][0]))
            ##Subtracting coordinates to get our height and them np.sum to convert it to a single value
            height = np.sum(np.subtract(result[0][2], result[0][1]))
            #By multiplying length*heights we can get the size of the region for our ocr text and then if that pass our region threshold then that should be our text
            # now if length*height is more than 60% of the entire plate region return that text(that is when we divide by rectangle_size)
            if length*height / rectangle_size > region_threshold:
                plate.append(result[1])
        return plate



    def ocrdetection(image_withdetect, detection_threshold, region_threshold):
        #^Grabs image with the detections
        scores = list(filter(lambda x: x> detection_threshold, detections['detection_scores']))
        #^Grabs the scores that pass the detection_threshold by looping through it
        boxes = detections['detection_boxes'][:len(scores)]
        #^Grabs everything that passes or is the same lenght as our scores array
        classes = detections['detection_classes'][:len(scores)]
        #Grabs Full Image Dimensions
        width = image_withdetect.shape[1]
        height = image_withdetect.shape[0]

        #FILTERING OUT OUR REGION OF INTEREST
        #EASYOCR
        #Now we loop through all the boxes in the boxes variable essentially grab each one if there are multiple detections
        #ind represents the index
        #box represents each box
        for ind, box in enumerate(boxes):
            #box represent the coordinates for the detection without respect to the actual image size
            roi = box*[height, width, height, width]
            #roi(multipied by height and width) coordinates with respect to the actual image size
            region = image_withdetect[int(roi[0]):int(roi[2]),int(roi[1]):int(roi[3])]
            #when loading images from opencv and visualizing them using matplob they need to be converted from BGR to RGB
            #to extract the region of interest some indexing was done
            #So we grabbed the images and passed our coordinated through it which we got from our roi(region of interest)
            #Filters by our x(Eg. roi[0]) and y(Eg. roi[2])
            #So we get only the region that represents our plate
            reader = easyocr.Reader(['en'], gpu = False)
            #Now we setup our easyocr reader with the language we will use
            ocr_result = reader.readtext(region)
            #print(ocr_result)
            #now we grab our result after using the reader on our region
            text = filter_text(region, ocr_result, region_threshold)
            #plt.imshow(cv2.cvtColor(region, cv2.COLOR_BGR2RGB))
            #and as said before we visualize it using pltimshow and pltshow
            #plt.show()
            return(text)

    finalres = ocrdetection(image_withdetect, detection_threshold, region_threshold)

    if finalres == []:
        #plt.imshow(cv2.cvtColor(image_np_with_detections, cv2.COLOR_BGR2RGB))
        #plt.savefig(os.path.join(paths['FLAGGEDPATH'],"myunidentifiedplate.jpg"))
        print("OCR failed to detect registration #")
        #return 'The result return is empty'
        raise Exception
    elif finalres == None:
        #plt.imshow(cv2.cvtColor(image_np_with_detections, cv2.COLOR_BGR2RGB))
        #plt.savefig(os.path.join(paths['FLAGGEDPATH'],"myunidentifiedplate.jpg"))
        print("OCR failed to detect registration #")
        raise Exception
        #return 'Error while detecting the licence plate on the image'
    else:
        finalres = finalres[0]
        return(finalres)
