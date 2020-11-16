/**
 *@file color_track.c
 *@brief infrastructure for analyzing results of ADC reads from IR sensors
 *to determine underlying colors
 *
 *(this does not deal with black detect for line following that occurs in zumo.c)
 */

#include "color_track.h"
#include "uart.h"
#include "leds.h"
//#include "zumo_rf.h"
#define NUM_COLORS 3

static struct ColorTrack graphite = {.low_bound = GREY_LOW, .high_bound = GREY_HIGH, .detect_thresh = 6};

//static struct ColorTrack purp = {.low_bound = PURP_LOW, .high_bound = PURP_HIGH, .detect_thresh = 1};


char buffer[50];
void detect_xc(uint32_t * vals)
{
//    //check for white traingle
    if (vals[0] < 500 && vals[1] < 500 && vals[2] < 500 && vals[3] < 500
            && vals[4] < 500 && vals[5] < 500)
    {
//        GPIO_toggleDio(BLED1);
        set_intersection_flag(1);
        GPIO_writeDio(BLED1,1);
    }
    return;
}

//void detect_poi(uint32_t * vals)
//{
//    if (vals[0] > (graphite.high_bound) && vals[1] > (graphite.high_bound) && vals[2] > (graphite.high_bound)
//            && vals[3] > (graphite.high_bound) && vals[4] > (graphite.high_bound) && vals[5] > (graphite.high_bound))
//    {
//        set_target_flag(1);
//        GPIO_toggleDio(IOID_15);
//        sprintf(buffer,"%u\r\n", vals[0]);
//        WriteUART0(buffer);
//    }
//    return;
//}

// && (get_xc_state()== 0b0100 || get_xc_state() == 0b0010)

void detect_poi(uint32_t * vals, int choice)
{
    graphite.left_accum = 0;
    graphite.left_stash_val = 0;

    graphite.right_accum = 0;
    graphite.right_stash_val = 0;

    graphite.left_prev_vals_ave = 0;
    graphite.right_prev_vals_ave = 0;

    graphite.left_prev_vals[graphite.idx] =
            (vals[3] > graphite.low_bound && vals[3] < graphite.high_bound) \
            + (vals[5] > graphite.low_bound && vals[5] < graphite.high_bound);
    graphite.right_prev_vals[graphite.idx] =
            (vals[2] > graphite.low_bound && vals[2] < graphite.high_bound) \
            + (vals[4] > graphite.low_bound && vals[4] < graphite.high_bound);


    int i;
    for (i = 0; i < NUM_PREV_VALS; i++)
    {
        graphite.left_prev_vals_ave += graphite.left_prev_vals[i];
        graphite.right_prev_vals_ave += graphite.right_prev_vals[i];

    }

    if (get_dist_flag() && (graphite.left_prev_vals_ave + graphite.right_prev_vals_ave > 5))
    {
        graphite.left_prev_vals_ave = 2;
        graphite.left_prev_vals_ave = 1;
    }

    graphite.idx = (graphite.idx + 1) % NUM_PREV_VALS;

    if (!get_detect_flag() && !get_actuation_flag())
    {
        if (graphite.left_prev_vals_ave + graphite.right_prev_vals_ave > graphite.detect_thresh)
        {
            set_detect_flag(1);
            GPIO_writeDio(BLED0,1);
//            GPIO_toggleDio(BLED0);
            for (i = 0; i < NUM_PREV_VALS; i++)
            {
                graphite.left_prev_vals[i] = 0;
                graphite.right_prev_vals[i] = 0;
            }
        }
    }

//    sprintf(buffer, "%u\r\n", graphite.left_prev_vals_ave + graphite.right_prev_vals_ave);
//    WriteUART0(buffer);
//    WriteRF(buffer);
//    if (graphite.left_prev_vals_ave + graphite.right_prev_vals_ave > 27
////            && !get_detect_flag()
//            && (get_xc_state()== 0b0100 || get_xc_state() == 0b0010))
//    {
//        set_target_flag(1);
//        GPIO_toggleDio(IOID_15);
//    }

    // In the case of moving target:
    // choice input 1: all black
    // choice input 2: left black
    // choice input 3: right black

    if (choice == 1){
        detect_all_black_target(vals);
    } else if (choice == 2){
        detect_left_black_target(vals);
    } else if (choice == 3){
        detect_right_black_target(vals);
    }

    return;
}

void detect_all_black_target(uint32_t * vals){
    uint8_t xc_state = get_xc_state();
    uint8_t prev_xc_state=  get_prev_xc_state();

    if (vals[0] > (graphite.high_bound) && vals[1] > (graphite.high_bound) && vals[2] > (graphite.high_bound)
                && vals[3] > (graphite.high_bound) && vals[4] > (graphite.high_bound) && vals[5] > (graphite.high_bound) && xc_state == prev_xc_state)
        {
            set_target_flag(1);
            //GPIO_toggleDio(IOID_15);
            SetAndWritePinHigh(BLED3);
            sprintf(buffer,"yeehaw all black targets");
            WriteUART0(buffer);
        }

}

void detect_left_black_target(uint32_t * vals){

    if (vals[0] > (graphite.high_bound) && vals[1] > (graphite.high_bound) && vals[2] > (graphite.high_bound)
                && vals[3] > (graphite.high_bound) && vals[4] < 500 && vals[5] > (graphite.high_bound) && !get_intersection_flag())
        {
            set_target_flag(1);
            //GPIO_toggleDio(IOID_15);
            SetAndWritePinHigh(BLED3);
            sprintf(buffer,"yeehaw left black targets");
            WriteUART0(buffer);
        }

}
void detect_right_black_target(uint32_t * vals){

    if (vals[0] > (graphite.high_bound) && vals[1] > (graphite.high_bound) && vals[2] > (graphite.high_bound)
                && vals[3] > (graphite.high_bound) && vals[4] > (graphite.high_bound) && vals[5] < 500 && !get_intersection_flag())
        {
            set_target_flag(1);
            //GPIO_toggleDio(IOID_15);
            SetAndWritePinHigh(BLED3);
            sprintf(buffer,"yeehaw right black targets");
            WriteUART0(buffer);
        }
}
