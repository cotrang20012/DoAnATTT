using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using FaceRecognition;

namespace FaceRecog
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        FaceRec faceRec = new FaceRec();

        private void button1_Click(object sender, EventArgs e)
        {
            faceRec.openCamera(pictureBox1, pictureBox2);
        }

        private void button2_Click(object sender, EventArgs e)
        {
            faceRec.Save_IMAGE(textBox1.Text);
        }

        private void button3_Click(object sender, EventArgs e)
        {
            faceRec.isTrained = true;
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            var files = Directory.GetFiles("C:\\Git\\DoAnATTT\\rieng tu\\HinhAnh");
            foreach(var file in files)
            {
                Console.WriteLine(file);
                pictureBox1.Image = Image.FromFile(file);
                faceRec
                faceRec.Save_IMAGE(file);
            }
        }
    }
}
