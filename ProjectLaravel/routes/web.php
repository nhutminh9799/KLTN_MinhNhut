<?php

use Illuminate\Support\Facades\Route;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

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
    ini_set('max_execution_time', 300);
    // $output = shell_exec("python testpy.py 2>&1");
    // $output = json_decode($output);
    // $output1 = shell_exec("cd ../ 2>&1");
    // $output1 = shell_exec("cd routes 2>&1");
    // shell_exec("cd /routes 2>&1");
    // $output = shell_exec("%CD% 2>&1");
    $output = shell_exec("python ProjectARIMA_LSTM\\main.py 2>&1");
    dd($output);
    return view('welcome');
});
