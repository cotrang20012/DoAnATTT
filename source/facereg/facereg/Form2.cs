using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using FaceRecognition;
namespace facereg
{
    public partial class Form2 : Form
    {
        FaceRec faceRec = new FaceRec();
        public Form2()
        {
            InitializeComponent();
            faceRec.openCamera(pictureBox1, pictureBox1);
        }

        private void button2_Click(object sender, EventArgs e)
        {
            faceRec.Save_IMAGE(textBox1.Text);
        }
    }
}
