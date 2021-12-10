using Emgu.CV;
using Emgu.CV.CvEnum;
using Emgu.CV.Face;
using Emgu.CV.Structure;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace facereg
{
    public partial class Form2 : Form
    {
        static List<Image<Gray, Byte>> TrainedFaces = new List<Image<Gray, byte>>();
        static List<int> PersonsLabes = new List<int>();
        static List<string> PersonsNames = new List<string>();
        private static bool isTrained = false;
        static EigenFaceRecognizer recognizer;
        public static Capture videoCapture = null;
        private Image<Bgr, Byte> currentFrame = null;
        private bool facesDetectionEnabled = true;
        bool EnableSaveImage = false;
        CascadeClassifier faceCasacdeClassifier = new CascadeClassifier(@"D:\source\facereg\facereg\bin\Debug\Haarcascade\haarcascade_frontalface_alt.xml");
        Mat frame = new Mat();
        public Form2()
        {
            if (videoCapture != null) videoCapture.Dispose();
            videoCapture = new Capture();
            InitializeComponent();
            
            //videoCapture.ImageGrabbed += ProcessFrame;
            Application.Idle += ProcessFrame;
        }

        private void button2_Click(object sender, EventArgs e)
        {
            button2.Enabled = false;
            EnableSaveImage = true;
        }
        private void ProcessFrame(object sender, EventArgs e)
        {
            //Step 1: Video Capture
            if (videoCapture != null && videoCapture.Ptr != IntPtr.Zero)
            {
                videoCapture.Retrieve(frame, 0);
                currentFrame = frame.ToImage<Bgr, Byte>().Resize(pictureBox1.Width, pictureBox1.Height, Inter.Cubic);

                //Step 2: Face Detection
                if (facesDetectionEnabled)
                {

                    //Convert from Bgr to Gray Image
                    Mat grayImage = new Mat();
                    CvInvoke.CvtColor(currentFrame, grayImage, ColorConversion.Bgr2Gray);
                    //Enhance the image to get better result
                    CvInvoke.EqualizeHist(grayImage, grayImage);

                    Rectangle[] faces = faceCasacdeClassifier.DetectMultiScale(grayImage, 1.1, 3, Size.Empty, Size.Empty);
                    //If faces detected
                    if (faces.Length > 0)
                    {

                        foreach (var face in faces)
                        {
                            //Draw square around each face 
                            // CvInvoke.Rectangle(currentFrame, face, new Bgr(Color.Red).MCvScalar, 2);
                            Image<Bgr, Byte> resultImage = currentFrame.Convert<Bgr, Byte>();
                            pictureBox2.SizeMode = PictureBoxSizeMode.StretchImage;
                            pictureBox2.Image = resultImage.Bitmap;
                            //Step 3: Add Person 
                            //Assign the face to the picture Box face picDetected
                            resultImage.ROI = face;
                            CvInvoke.Rectangle(currentFrame, face, new Bgr(Color.Red).MCvScalar, 2);

                            if (EnableSaveImage)
                            {
                                //We will create a directory if does not exists!
                                string path = Directory.GetCurrentDirectory() + @"\Image";
                                if (!Directory.Exists(path))
                                    Directory.CreateDirectory(path);
                                //we will save 10 images with delay a second for each image 
                                //to avoid hang GUI we will create a new task
                                Task.Factory.StartNew(() => {
                                    for (int i = 0; i < 10; i++)
                                    {
                                        //resize the image then saving it
                                        resultImage.Resize(100, 100, Inter.Cubic).Save(path + @"\" + textBox1.Text + ".jpg");
                                        Thread.Sleep(1000);
                                    }
                                });

                            }
                            EnableSaveImage = false;

                            if (button2.InvokeRequired)
                            {
                                button2.Invoke(new ThreadStart(delegate {
                                    button2.Enabled = true;
                                }));
                            }

                            
                            
                        }
                    }
                }

                //Render the video capture into the Picture Box picCapture
                pictureBox1.Image = currentFrame.Bitmap;
            }

            //Dispose the Current Frame after processing it to reduce the memory consumption.
            if (currentFrame != null)
                currentFrame.Dispose();
        }
    }
    
}
