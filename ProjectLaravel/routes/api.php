<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ModelController;
use App\Http\Controllers\BitcoinController;
use App\Http\Controllers\EthereumController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::middleware('auth:api')->get('/user', function (Request $request) {
    return $request->user();
});

Route::get('/getValue',[ModelController::class, 'getModel']);

//API BTC
Route::get('/getAllBTC',[BitcoinController::class,'getAll']);
Route::get('/getQLearningBTC',[BitcoinController::class,'getQLearningGraph']);
Route::get('/getPredictPriceBTC',[BitcoinController::class,'getPredictPrice']);
Route::get('/getNewDataBTC',[BitcoinController::class,'getNewData']);
Route::get('/getDataBTC',[BitcoinController::class,'getData']);
Route::get('/cloneInfo',[BitcoinController::class,'cloneInfo']);

//API ETH
Route::get('/getAllETH',[EthereumController::class,'getAll']);
Route::get('/getQLearningETH',[EthereumController::class,'getQLearningGraph']);
Route::get('/getPredictPriceETH',[EthereumController::class,'getPredictPrice']);
Route::get('/getNewDataETH',[EthereumController::class,'getNewData']);
Route::get('/getDataETH',[EthereumController::class,'getData']);
