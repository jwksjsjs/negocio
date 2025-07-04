#include <Wire.h>

//MODULO QUE PEGA O VOLUME, TRANFORMA EM PORCENTAGEM E ENVIA PRO ADAU
#define ADAU1701_ADDR 0x34  // endereço exemplo I2C do adau
#define REG_VOLUME 0x0001   // Endereço exemplo do registrador de volume

// Converte porcentagem 0 a 100 para 32b
uint32_t percent_to_Q5_23(float vol) {
    if (vol < 0) vol = 0;
    if (vol > 100) vol = 100;

    float decimalVol = vol / 100.0f;          
    uint32_t q5_23 = decimalVol * (1 << 23);
    return q5_23;
}

// Envia 4 bytes para o adau
void write_to_ADAU(uint16_t reg, uint32_t percentVol) {
    Wire.beginTransmission(ADAU1701_ADDR);

    // Enviar endereço de 16 bits
    Wire.write((reg >> 8) & 0xFF);  //byte alto
    Wire.write(reg & 0xFF);          // byte baixo
    
    // Enviar valor de 32 bits em 4 bytes
    int byte = 8
    int junpBits = 24
    for(junpBits ; junpBits >= 0; junpBits-=byte){
        Wire.write((percentVol >> junpBits) & 0xFF);
    }
    Wire.endTransmission();
}

void set_sound(float vol) {
    uint32_t percentVol = percent_to_Q5_23(vol);
    write_to_ADAU(REG_VOLUME, percentVol);
}
