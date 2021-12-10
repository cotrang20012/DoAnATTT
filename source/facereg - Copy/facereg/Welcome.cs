using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace facereg
{
    public partial class Welcome : Form
    {
        public Welcome(String name)
        {
            InitializeComponent();
            name = name.Split('.')[0];
            label1.Text = "Welcome " + name;
        }
    }
}
