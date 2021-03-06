<?php

namespace App\Http\Controllers;

use App\Models\EthereumModel;
use Carbon\Carbon;
use GuzzleHttp\Client;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;


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

    public static function getQLearningGraph()
    {
        ini_set('max_execution_time', 300);
        $output = shell_exec("python ProjectQLearningETH\\main.py 2>&1");
    }

    public function getPredictPrice()
    {
        ini_set('max_execution_time', 300);
        $output = shell_exec("python ProjectARIMA_LSTM_ETH\\main.py 2>&1");
        if (!($fp = fopen('DuBaoETH.csv', 'r'))) {
            die("Can't open file...");
        }

        //read csv headers
        $key = fgetcsv($fp,"1024",",");

        // parse csv rows into array
        $json = array();
        while ($row = fgetcsv($fp,"1024",",")) {
            $json[] = array_combine($key, $row);
        }

        // release file handle
        fclose($fp);
        // encode array to json
        foreach($json as $row){
            EthereumModel::where('datetime_eth', $row["datetime_eth"])
                ->update(['predict_hybrid_arima_lstm' => $row["Final_LSTM"]]);
        }
        return json_encode($json);
    }

    public function getData(){
        return EthereumModel::orderBy('id', 'desc')->take(100)->get();
    }

    public function getNewData(){
        //Session get date current
        $dt = Carbon::now();
        $dt = $dt->toDateString();
        DB::table('ethereum')->insert([
            'datetime_eth' => $dt
        ]);
        //Session Update closing price previous day
        $dateNow = date('Y-m-d', strtotime(' -1 day'));
        $client = new Client();
        $content = file_get_contents('https://www.cnbc.com/quotes/ETH=');
        preg_match('#<li class="Summary-stat Summary-prevClose"><span class="Summary-label">Prev Close</span><span class="Summary-value">(.*)</span></li>#', $content, $match);
        $partern = '/,/';
        $replacement = '';
        $price = preg_replace($partern, $replacement, $match[1]);
        $price =  floatval($price);
        EthereumModel::where('datetime_eth', $dateNow)
            ->update(['closing_price' => $price]);
    }
}
