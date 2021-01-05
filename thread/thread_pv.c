# include<stdio.h>
# include<pthread.h>
# include<semaphore.h>

static int balance = 0;
static sem_t sem1;

void *
deposit(void *args) {
    sem_wait(&sem1);
    balance += 1;
    sem_post(&sem1);
    return NULL;
}

void *
withdraw(void *args) {
    sem_wait(&sem1);
    balance -= 1;
    sem_post(&sem1);
    return NULL;
}

void
threadDemo() {
    int n = 10000;
    pthread_t tid1[n];
    pthread_t tid2[n];
    int ret1 = sem_init(&sem1, 0, 1);
    printf("ret1 %d \n",ret1);
    int offset = -1;
    for (int i = 0; i < n; i ++) {
        pthread_create(&tid1[i], NULL, deposit, NULL);
        pthread_create(&tid2[i], NULL, withdraw, NULL);
    }
    for (int i = 0; i < n; i ++) {
        pthread_join(tid1[i], NULL);
        pthread_join(tid2[i], NULL);
    }
    sem_destroy(&sem1);
    printf("balance %d\n", balance);
}

int
main(){
    threadDemo();
    return 0;
}