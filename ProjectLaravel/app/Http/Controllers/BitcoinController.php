<?php

namespace App\Http\Controllers;

use Carbon\Carbon;
use Illuminate\Http\Request;
use App\Models\BitcoinModel;
use GuzzleHttp\Client;
use Illuminate\Support\Facades\DB;

class BitcoinController extends Controller
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

    /**
     * Get All Data Convert to CSV
     */
    public function getAll()
    {
        $json = BitcoinModel::all();
        $json_obj = json_decode ($json);

        $fp = fopen('BTC.csv', 'w');
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

    /**
     * Get QLearning Graph BTC
     */
    public static function getQLearningGraph()
    {
        ini_set('max_execution_time', 300);
        $output = shell_exec("python3 ProjectQLearningBTC/main.py 2>&1");
    }

    public function getPredictPrice()
    {
        ini_set('max_execution_time', 300);
        $output = shell_exec("python3 ProjectARIMA_LSTM_BTC/main.py 2>&1");
        if (!($fp = fopen('DuBao.csv', 'r'))) {
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
            BitcoinModel::where('datetime_btc', $row["datetime_btc"])
                ->update(['predict_hybrid_arima_lstm' => $row["Final_LSTM"]]);
        }
        return json_encode($json);
    }

    /**
     * Function get 100 data gần nhất
     *
     * @return mixed
     */
    public function getData(){
        return BitcoinModel::orderBy('id', 'desc')->take(50)->get();
    }

    public function getNewData(){
        //Session get date current
        $dt = Carbon::now();
        $dt = $dt->toDateString();
        DB::table('bitcoin')->insert([
            'datetime_btc' => $dt
        ]);
        //Session Update closing price previous day
        $dateNow = date('Y-m-d', strtotime(' -1 day'));
        $client = new Client();
        $res = $client->get('https://api.coindesk.com/v1/bpi/historical/close.json?start='.$dateNow.'&end='.$dateNow);
        $a = $res->getBody()->getContents();
        $a = json_decode($a);
        $real_price = $a->bpi->$dateNow;
        BitcoinModel::where('datetime_btc', $dateNow)
            ->update(['closing_price' => $real_price]);
    }

    /**
     * Clone Information
     *
     */
    public function cloneInfo(){
        $client = new Client();
        $res = $client->get('https://api.coindesk.com/v1/bpi/currentprice/USD.json');
        $a = $res->getBody()->getContents();
        $a = json_decode($a);
        $real_price = $a->bpi->USD->rate;

        $content = file_get_contents('https://www.coindesk.com/price/bitcoin');
        preg_match('#<span class="percent-value-text">-1.84</span>#', $content, $match);
        $gross = $match[1];
        $info = null;
        $info->real_price = $real_price;
        $info->gross = $gross;
        $JsonInfo = json_decode($info);

        return $JsonInfo;

    }
}
