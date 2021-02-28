#!/usr/bin/perl

while(<>) {

    chomp($_);
    @y[$i] = $_;
    # printf("%.3f\n", $y[$i]);
    $i++;

}

$cushion = 1;
$max_y = $i-1;
$min_y = 0;
$max_s = $max_y - $cushion;
$min_s = $cushion;

$best_difference = $best_abs_log_ratio = 0;
$best_dev_sum = 1000000;

# printf("max_y = %d\n", $max_y);

for($s=$min_s; $s<=$max_s; $s++) {

    $mass1 = $mass2 = $dev1 = $dev2 = 0;

    for($i2=$min_y; $i2<=$s; $i2++) {      # Include split point in the first half
	$mass1 += $y[$i2];
    }
    $avg1 = $mass1/(($s-$min_y)+1);
    for($i2=$min_y; $i2<=$s; $i2++) {      # Include split point in the first half
	$dev1 += ($y[$i2] - $avg1) ** 2;
    }

    for($i2=$s+1; $i2<=$max_y; $i2++) {
	$mass2 += $y[$i2];
    }
    $avg2 = $mass2/($max_y - $s);
    for($i2=$s+1; $i2<=$max_y; $i2++) {
	$dev2 += ($y[$i2] - $avg2) ** 2;
    }
    
    $difference = $avg2 - $avg1;
    $log_ratio = log($avg2 / $avg1);
    $dev_sum = $dev1 + $dev2;
    printf("%d: avg1 = %.3f; avg2 = %.3f; diff = %.3f, ratio = %.3f, log ratio = %.3f, dev1 = %.3f, dev2 = %.3f, dev sum = %.3f\n", $s, $avg1, $avg2, $difference, $avg2 / $avg1, $log_ratio, $dev1, $dev2, $dev_sum);
    if(abs($difference) > $best_abs_difference) {
	$best_abs_difference = abs($difference);
	$best_difference = $difference;
	$best_diff_split_point = $s;
    }
    if(abs($log_ratio) > $best_abs_log_ratio) {
	$best_abs_log_ratio = abs($log_ratio);
	$best_log_ratio = $log_ratio;
	$best_ratio_split_point = $s;
    }
    if($dev_sum < $best_dev_sum) {
	$best_dev_sum = $dev_sum;
	$best_dev_split_point = $s;
	$best_mean1 = $avg1;
	$best_mean2 = $avg2;
    }
}

printf("Max absolute difference = %.3f (%.3f), split point = %d\n", $best_abs_difference, $best_difference, $best_diff_split_point);
printf("Max abs log ratio = %.3f (%.3f), split point = %d\n", $best_abs_log_ratio, $best_log_ratio, $best_ratio_split_point);
printf("Min summed squared deviations = %.3f, split point = %d, mean1 = %.3f, mean2 = %.3f\n", $best_dev_sum, $best_dev_split_point, $best_mean1, $best_mean2);
