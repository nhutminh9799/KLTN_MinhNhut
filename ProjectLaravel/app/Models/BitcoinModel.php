<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class BitcoinModel extends Model
{
    use HasFactory;
    protected $table = 'bitcoin';
    public $timestamps = false;
}
