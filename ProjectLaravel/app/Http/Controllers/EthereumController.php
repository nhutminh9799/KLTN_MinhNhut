<?php

namespace App\Http\Controllers;

use App\Models\BitcoinModel;
use Illuminate\Http\Request;
use App\Models\EthereumModel;

class EthereumController extends Controller
{
    /**
     * Handle the incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function __invoke(Request $request)
    {
        //
    }
    public function getAll()
    {
        $json = EthereumModel::all();
        $json_obj = json_decode ($json);

        $fp = fopen('ETH.csv', 'w');
        $keys = array();
        foreach($json_obj[0] as $key => $val) {
            $keys[]= $key;
        }
        fputcsv($fp, (array) $keys);
        foreach ($json_obj as $fields) {
            fputcsv($fp, (array) $fields);
        }

        fclose($fp);
    }
}
