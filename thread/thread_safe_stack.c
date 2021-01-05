#include<pthread.h>

//static pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

struct stack{
    int data[100];
    int top;
};

typedef struct stack Stack;
//创建栈
Stack s;

void
init() {
    s.top = -1;
}

void
push(element) {
//     pthread_mutex_lock(&mutex);
    if(s.top > 98) {
        printf("full!!!!\n");
    } else {
        s.top += 1;
        s.data[s.top] = element;
        printf("push %d top is %d\n", s.data[s.top], s.top);
    }
//     pthread_mutex_unlock(&mutex);
}

void
pop() {
//     pthread_mutex_lock(&mutex);
    if(s.top < 0) {
        printf("empty!!!!\n");
    } else {
        printf("pop %d top is %d\n", s.data[s.top], s.top);
        s.data[s.top] = 0;
        s.top -= 1;
    }
//     pthread_mutex_unlock(&mutex);
}

void run() {
    push(2);
    pop();
}

int top() {
    return s.top;
}

void
threadDemo() {
    int n = 500;
    pthread_t tid1[n];
////    pthread_t tid2[n];
    for (int i = 0; i < n; i ++) {
        pthread_create(&tid1[i], NULL, run, NULL);
    }
    for (int i = 0; i < n; i ++) {
        pthread_join(tid1[i], NULL);
    }
//    run();

}

int main()
{
    threadDemo();
    int v = top();
    printf("thread top%d\n", v);
}
