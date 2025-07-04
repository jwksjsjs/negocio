#include <Wire.h>

//MODULO QUE PEGA O VOLUME, TRANFORMA EM PORCENTAGEM E ENVIA PRO ADAU
#define ADAU1701_ADDR 0x34  // endereço exemplo I2C do adau
#define REG_VOLUME 0x0001   // Endereço exemplo do registrador de volume

// Converte porcentagem 0 a 100 para 32b
uint32_t percent_to_Q5_23(float percent) {
    if (percent < 0) percent = 0;
    if (percent > 100) percent = 100;

    float decimal = percent / 100.0f;          
    uint32_t q5_23 = decimal * (1 << 23);
    return q5_23;
}

// Envia 4 bytes para o adau
void write_to_ADAU(uint16_t reg, uint32_t value) {
    Wire.beginTransmission(ADAU1701_ADDR);

    // Enviar endereço de 16 bits
    Wire.write((reg >> 8) & 0xFF);  //byte alto
    Wire.write(reg & 0xFF);          // byte baixo

    // Enviar valor de 32 bits em 4 bytes
    for(int i = 24; i > 0; i){
        Wire.write((value >> i) & 0xFF);
        i = i-8
    }
    Wire.endTransmission();
}

void set_sound(float percent) {
    uint32_t qValue = percent_to_Q5_23(percent);
    write_to_ADAU(REG_VOLUME, qValue);
}
