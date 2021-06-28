<?php

namespace App\Console;

use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;

class Kernel extends ConsoleKernel
{
    /**
     * The Artisan commands provided by your application.
     *
     * @var array
     */
    protected $commands = [
        //
    ];

    /**
     * Define the application's command schedule.
     *
     * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
     * @return void
     */
    protected function schedule(Schedule $schedule)
    {
        // $schedule->command('inspire')->hourly();
        //function cron new data
        $schedule->call(function () {
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, "http://127.0.0.1:8000/api/getNewDataBTC");
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_exec($ch);
            curl_close($ch);

            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, "http://127.0.0.1:8000/api/getNewDataETH");
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_exec($ch);
            curl_close($ch);
        })->dailyAt('00:30');

        //function export data to csv
        $schedule->call(function () {
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, "http://127.0.0.1:8000/api/getAllBTC");
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_exec($ch);
            curl_close($ch);

            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, "http://127.0.0.1:8000/api/getAllETH");
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_exec($ch);
            curl_close($ch);
        })->dailyAt('00:45');

        //function Q-Learning
        $schedule->call(function () {
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, "http://127.0.0.1:8000/api/getQLearningBTC");
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_exec($ch);
            curl_close($ch);

            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, "http://127.0.0.1:8000/api/getQLearningETH");
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_exec($ch);
            curl_close($ch);
        })->dailyAt('1:20');

        //fucntion predicted price
        $schedule->call(function () {
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, "http://127.0.0.1:8000/api/getPredictPriceBTC");
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_exec($ch);
            curl_close($ch);

            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, "http://127.0.0.1:8000/api/getPredictPriceETH");
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_exec($ch);
            curl_close($ch);
        })->weeklyOn(2, '3:00');
    }

    /**
     * Register the commands for the application.
     *
     * @return void
     */
    protected function commands()
    {
        $this->load(__DIR__.'/Commands');

        require base_path('routes/console.php');
    }
}
