<?php

use Illuminate\Support\Facades\Route;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;
use App\Http\Controllers\BitcoinController;
use App\Http\Controllers\EthereumController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/


Route::get('/', function () {
//    ini_set('max_execution_time', 300);
    // $output = shell_exec("python testpy.py 2>&1");
    // $output = json_decode($output);
    // $output1 = shell_exec("cd ../ 2>&1");
    // $output1 = shell_exec("cd routes 2>&1");
    // shell_exec("cd /routes 2>&1");
    // $output = shell_exec("%CD% 2>&1");

//    $output = shell_exec("python ProjectARIMA_LSTM_BTC\\main.py 2>&1");
//    dd($output);
//    return view('welcome');
});

Route::get('/getAllBTC',[BitcoinController::class,'getAll']);
Route::get('/getAllETH',[EthereumController::class,'getAll']);
Route::get('/getQLearningBTC',[BitcoinController::class,'getQLearningGraph']);
Route::get('/getPredictPriceBTC',[BitcoinController::class,'getPredictPrice']);
Route::get('/get10',[BitcoinController::class,'getData']);
