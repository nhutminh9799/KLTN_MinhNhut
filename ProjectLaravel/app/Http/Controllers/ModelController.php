<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class ModelController extends Controller
{
    //
    public function getModel(){
        $cols = ["Date","Closing_Price","ARIMA","Error","Date","Error_pred","ARIMA_LSTM"];
        $csv = file('.././public/LSTM_Model.csv');
        $output = [];
        
        foreach ($csv as $line_index => $line) {
            if ($line_index > 0) { // I assume the the first line contains the column names.
                $newLine = [];
                $values = explode(',', $line);
                foreach ($values as $col_index => $value) {
                    $newLine[$cols[$col_index]] = $value;
                }
                $output[] = $newLine;
            }
        }
        
        $json_output = json_encode($output);
        return $json_output;
    }
}
