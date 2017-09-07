<?
        // Global Variables
        $image_dir = "./"; // directory on server
        $image_relative_path = './; // path to images relative to script
        $file_types = array('jpg', 'jpeg', 'gif', 'png');
        $image_time = '4000'; // seconds each image will display (4000 = 4 seconds)
        $image_rotation ='';
        if ($handle = opendir($image_dir)) {
            while (false !== ($file = readdir($handle))) {
                if ($file != "." && $file != "..") {
                    $ext_bits = explode(".", $file); // finds file extensions
                    foreach ($ext_bits as $key => $value) {
                        if (in_array($value, $file_types)) {
                            $image_rotation .= '<li><img src="' .base_url().$image_relative_path . '/' . $file . '"></li>';
                        }
                    }
                }
            }
            closedir($handle);
        }
        ?>
