#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#define GPIO_OUTPUT_IO 4
#define GPIO_OUTPUT_PIN_SEL (1ULL<<GPIO_OUTPUT_IO)
#define GPIO_BUTTON_IO 2
#define GPIO_BUTTON_PIN_SEL (1ULL<<GPIO_BUTTON_IO)
void vTask(void * pvParameters)
{
    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_DISABLE;
    //set as output mode
    io_conf.mode = GPIO_MODE_INPUT;
    //bit mask of the pins that you want to set
    io_conf.pin_bit_mask = GPIO_BUTTON_PIN_SEL;
    //disable pull-down mode
    io_conf.pull_down_en = 0;
    //disable pull-up mode
    io_conf.pull_up_en = 0;
    //configure GPIO with the given settings
    gpio_config(&io_conf);

    static int button_count = 0;
    int last_button = 1;
    while (1) {
        int current_button = gpio_get_level(GPIO_BUTTON_IO);
        if (last_button ==1 && current_button ==0)
        {
            button_count++;
            printf("Buton apasat %d\n", button_count);
        }
        last_button = current_button;
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}

void app_main() {
    //zero-initialize the config structure.
    gpio_config_t io_conf = {};
    //disable interrupt
    io_conf.intr_type = GPIO_INTR_DISABLE;
    //set as output mode
    io_conf.mode = GPIO_MODE_OUTPUT;
    //bit mask of the pins that you want to set
    io_conf.pin_bit_mask = GPIO_OUTPUT_PIN_SEL;
    //disable pull-down mode
    io_conf.pull_down_en = 0;
    //disable pull-up mode
    io_conf.pull_up_en = 0;
    //configure GPIO with the given settings
    gpio_config(&io_conf);
    
    int cnt = 0;
    while(1) {
        printf("cnt: %d\n", cnt++);
        if(cnt % 4 == 0)
        {
            gpio_set_level(GPIO_OUTPUT_IO, 1);
            vTaskDelay(750 / portTICK_PERIOD_MS);
        }
        if(cnt % 4 == 1)
        {
            gpio_set_level(GPIO_OUTPUT_IO, 0);
            vTaskDelay(1000 / portTICK_PERIOD_MS);
        }
        if(cnt % 4 == 2)
        {
            gpio_set_level(GPIO_OUTPUT_IO, 1);
            vTaskDelay(500 / portTICK_PERIOD_MS);
        }
        if(cnt % 4 == 3)
        {
            gpio_set_level(GPIO_OUTPUT_IO, 0);
            vTaskDelay(250 / portTICK_PERIOD_MS);
        }
    }
}

/* 
    Ce rol are functia gpio config?
gpio_config are rol de a configura GPIO4 ca si port de iesire. 

    In codul exemplu, pinul GPIO4 este configurat ca iesire. Care sunt celelalte
moduri ın care poate fi configurat un pin GPIO?
GPIO4 poate fi configurat ca si pull-up/pull-down, iesire/intrare, pin mapping


    Explicati apelul vTaskDelay.
apelul functii vTaskDelay este pentru a creea o pauza pentru a observa cand ledul este activ si inactiv. 
    De ce functia principala se numeste app main?
*/